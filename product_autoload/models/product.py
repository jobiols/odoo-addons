# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.template"

    item_code = fields.Char(
        help="Code from bulonfer, not shown",
        select=1
    )

    upv = fields.Integer(
        help='Agrupacion mayorista'
    )

    wholesaler_bulk = fields.Integer(
        help="Bulk Wholesaler quantity of units",
    )

    retail_bulk = fields.Integer(
        help="Bulk retail quantity of units",
    )

    invalidate_category = fields.Boolean(
        help="Category needs rebuild",
        default=False
    )

    difference = fields.Float(
        help="Difference % in cost price between invoce and system, "
             "calculated as (invoice_price-system_price)/invoice_price"
             "this diference is an error and must go towars zero."
    )

    system_cost = fields.Float(
        compute="_compute_system_cost"
    )

    margin = fields.Float(
        help="bulonfer margin for this product"
    )

    @api.multi
    def _compute_system_cost(self):
        for prod in self:
            prod.system_cost = prod.standard_price / (
                1 - prod.difference / 100)

    @api.multi
    def recalculate_list_price(self, margin):
        """ Recalcula los precios, verificando el precio que cargaron en la
            factura de compra. Estoy seguro de que son solo compras a bulonfer
            porque son las unicas que tienen discount_processed en True.
        """

        # buscar la linea de factura de compra que tiene el producto
        invoice_lines_obj = self.env['account.invoice.line']
        for prod in self:
            invoice_line = invoice_lines_obj.search(
                [('product_id.default_code', '=', prod.default_code),
                 ('invoice_id.discount_processed', '=', True)],
                order="id desc",
                limit=1)

            p_dif = False
            if invoice_line and invoice_line.price_unit:
                # precio que cargaron en la factura de compra
                invoice_price = invoice_line.price_unit
                # descuento en la linea de factura
                invoice_price *= (1 - invoice_line.discount / 100)
                # descuento global en la factura
                invoice_price *= (1 + invoice_line.invoice_discount)
                # descuento por nota de credito al final del mes
                invoice_price *= (1 - 0.05)

                # precio que vino de bulonfer (puede ser cero)
                system_price = prod.standard_price
                if system_price:
                    p_dif = (invoice_price - system_price) / invoice_price

            p_dif *= 100
            prod.write({
                'list_price': prod.standard_price * (1 + margin),
                'margin': margin * 100,
                'difference': p_dif
            })
