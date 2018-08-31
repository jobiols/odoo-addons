# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, fields, models, _, SUPERUSER_ID
from openerp.tools.float_utils import float_compare, float_round
from datetime import datetime
from openerp.exceptions import UserError, AccessError
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT

#from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
#from openerp.tools.translate import _
#from openerp.tools.translate import _
#from openerp import SUPERUSER_ID, api, models
#from openerp.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    price_product_unit = fields.Float(
        help="Technical field used to record the product cost set by the user "
             "during a picking confirmation (when costing method used is "
             "'average price' or 'real'). Value given in PRODUCT currency and "
             "in product uom.")

    # as it's a technical field, we intentionally don't provide the digits
    # attribute

    def get_price_unit(self, cr, uid, move, context=None):
        """ Returns the unit price to store on the quant """
        if move.purchase_line_id:
            order = move.purchase_line_id.order_id
            # if the currency of the PO is different than the company one, the
            # price_unit on the move must be reevaluated
            # (was created at the rate of the PO confirmation, but must be
            # valuated at the rate of stock move execution)
            if order.currency_id != move.company_id.currency_id:
                # we don't pass the move.date in the compute() for the currency
                # rate on purpose because
                # 1) get_price_unit() is supposed to be called only through
                #    move.action_done(),
                # 2) the move hasn't yet the correct date (currently it is the
                #    expected date, after completion of action_done() it will
                #    be now() )
                price_unit, price_product_unit = \
                    move.purchase_line_id._get_stock_move_price_unit()
                move.write({
                    'price_unit': price_unit,
                    'price_product_unit': price_product_unit
                })
                return price_unit, price_product_unit
            return move.price_unit
        return super(StockMove, self).get_price_unit(cr, uid, move,
                                                     context=context)

    def _store_average_cost_price(self, cr, uid, move, context=None):
        """ move is a browe record
            aqui le agregamos el costo en la moneda del producto
        """
        product_obj = self.pool.get('product.product')
        if any([q.qty <= 0 for q in move.quant_ids]) or move.product_qty == 0:
            # if there is a negative quant,
            # the standard price shouldn't be updated
            return
        # Note: here we can't store a quant.cost directly as we may have moved
        # out 2 units (1 unit to 5€ and 1 unit to 7€) and in case of a product
        # return of 1 unit, we can't know which of the 2 costs has to be used
        # (5€ or 7€?). So at that time, thanks to the average valuation price
        # we are storing we will valuate it at 6€
        average_valuation_price = 0.0
        average_prod_val_price = 0.0
        for q in move.quant_ids:
            average_valuation_price += q.qty * q.cost
            average_prod_val_price += q.qty * q.cost_product
        average_valuation_price = average_valuation_price / move.product_qty
        average_prod_val_price = average_prod_val_price / move.product_qty
        # Write the standard price, as SUPERUSER_ID because a warehouse manager
        # may not have the right to write on products
        ctx = dict(context or {}, force_company=move.company_id.id)
        product_obj.write(cr, SUPERUSER_ID,
                          [move.product_id.id], {
                              'standard_price': average_valuation_price,
                              'standard_product_price': average_prod_val_price
                          }, context=ctx)
        self.write(cr, uid, [move.id], {
            'price_unit': average_valuation_price,
            'price_product_unit': average_prod_val_price
        },
                   context=context)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    cost_product = fields.Float(
        help="Technical field used to record the product cost in product currency"
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='product_tmpl_id.currency_id',
        readonly=True,
        help="Product currency"
    )

    def _quant_create(self, cr, uid, qty, move, lot_id=False, owner_id=False,
                      src_package_id=False, dest_package_id=False,
                      force_location_from=False, force_location_to=False,
                      context=None):
        """ Create a quant in the destination location and create a negative
            quant in the source location if it's an internal location.
        """
        if context is None:
            context = {}
        price_unit, price_product_unit = self.pool.get(
            'stock.move').get_price_unit(cr, uid, move, context=context)
        location = force_location_to or move.location_dest_id
        rounding = move.product_id.uom_id.rounding
        vals = {
            'product_id': move.product_id.id,
            'location_id': location.id,
            'qty': float_round(qty, precision_rounding=rounding),
            'cost': price_unit,
            'cost_product': price_product_unit,
            'history_ids': [(4, move.id)],
            'in_date': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            'company_id': move.company_id.id,
            'lot_id': lot_id,
            'owner_id': owner_id,
            'package_id': dest_package_id,
        }
        if move.location_id.usage == 'internal':
            # if we were trying to move something from an internal location
            # and reach here (quant creation), it means that a negative quant
            # has to be created as well.
            negative_vals = vals.copy()
            negative_vals[
                'location_id'] = force_location_from and force_location_from.id or move.location_id.id
            negative_vals['qty'] = float_round(-qty,
                                               precision_rounding=rounding)
            negative_vals['cost'] = price_unit
            negative_vals['negative_move_id'] = move.id
            negative_vals['package_id'] = src_package_id
            negative_quant_id = self.create(cr, SUPERUSER_ID, negative_vals,
                                            context=context)
            vals.update({'propagated_from_id': negative_quant_id})

        picking_type = move.picking_id and move.picking_id.picking_type_id or False
        if lot_id and move.product_id.tracking == 'serial' and (
                not picking_type or (
                    picking_type.use_create_lots or picking_type.use_existing_lots)):
            if qty != 1.0:
                raise UserError(_('You should only receive by the piece with the same serial number'))

        # create the quant as superuser, because we want to restrict the
        # creation of quant manually: we should always use this method to
        # create quants
        quant_id = self.create(cr, SUPERUSER_ID, vals, context=context)
        return self.browse(cr, uid, quant_id, context=context)

    @api.model
    def stock_fix_cost(self):
        """ Para ejecutar a mano calcula los costos en dolares basado en los
            costos en pesos
        """
        company_currency_obj = self.env['res.currency']
        cc = company_currency_obj.search([('name', '=', 'ARS')])

        # stock quant
        stock_quant_obj = self.env['stock.quant']
        stock_quant = stock_quant_obj.search([('cost', '!=', 0)])
        for sq in stock_quant:
            _logger.info('FIXING quant %d %s' % (sq.product_id.product_tmpl_id.currency_id.id,sq.product_id.default_code))
            sq.cost_product = cc.with_context(
                {'date': sq.in_date}).compute(
                sq.cost, sq.product_id.product_tmpl_id.currency_id,
                round=False
            )

        # stock.move
        stock_move = self.env['stock.move'].search([('price_unit', '!=', 0)])
        for sm in stock_move:
            _logger.info('FIXING move %d %s' % (sm.product_id.product_tmpl_id.currency_id.id, sm.product_id.default_code))
            sm.price_product_unit = cc.with_context(
                {'date': sm.create_date}).compute(
                sm.price_unit, sm.product_id.product_tmpl_id.currency_id,
                round=False)
