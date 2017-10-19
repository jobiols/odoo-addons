# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp.osv import fields, osv


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    _columns = {
        'route_id': fields.many2one('stock.location.route', required=True)
    }

    def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
                                  uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                                  lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False,
                                  flag=False, warehouse_id=False, context=None):
        context = context or {}
        product_uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        warning = {}
        # UoM False due to hack which makes sure uom changes price, ... in product_id_change
        res = self.product_id_change(cr, uid, ids, pricelist, product, qty=qty,
                                     uom=False, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                                     lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
                                     fiscal_position=fiscal_position, flag=flag, context=context)

        if not product:
            res['value'].update({'product_packaging': False})
            return res

        # set product uom in context to get virtual stock in current uom
        if 'product_uom' in res.get('value', {}):
            # use the uom changed by super call
            context = dict(context, uom=res['value']['product_uom'])
        elif uom:
            # fallback on selected
            context = dict(context, uom=uom)

        # update of result obtained in super function
        product_obj = product_obj.browse(cr, uid, product, context=context)
        res['value'].update(
                {'product_tmpl_id': product_obj.product_tmpl_id.id, 'delay': (product_obj.sale_delay or 0.0)})

        # Calling product_packaging_change function after updating UoM
        res_packing = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging,
                                                    context=context)
        res['value'].update(res_packing.get('value', {}))
        warning_msgs = res_packing.get('warning') and res_packing['warning']['message'] or ''

        if product_obj.type == 'product':
            # determine if the product needs further check for stock availibility
            is_available = self._check_routing(cr, uid, ids, product_obj, warehouse_id, context=context)

            # check if product is available, and if not: raise a warning, but do this only for products
            # that aren't processed in MTO
            if not is_available:
                uom_record = False
                if uom:
                    uom_record = product_uom_obj.browse(cr, uid, uom, context=context)
                    if product_obj.uom_id.category_id.id != uom_record.category_id.id:
                        uom_record = False
                if not uom_record:
                    uom_record = product_obj.uom_id

                # verificar si en algun lado hay, si no hay damos el warning aunque lo dejamos vender igual
                compare_qty = float_compare(product_obj.virtual_available, qty, precision_rounding=uom_record.rounding)
                if compare_qty == -1:
                    warn_msg = _('Intenta vender {} Un pero solo tiene {} Un disponibles !\n'
                                 'El stock real es {} Un. (sin reservas)').format(
                            int(qty),
                            int(max(0, product_obj.virtual_available)),
                            int(max(0, product_obj.qty_available)))
                    warning_msgs += _("No hay suficiente stock !\n\n") + warn_msg + "\n\n"

                # verificar donde está el producto y si está en otro local sacamos otro warning
                locations = self.calc_formated_stock(cr, uid, ids, product_obj, context)
                if locations:
                    warning_msgs += locations

        # update of warning messages
        if warning_msgs:
            warning = {
                'title': u'Advertencia',
                'message': warning_msgs
            }
        res.update({'warning': warning})
        return res

    @api.multi
    def calc_virtual_stock(self, product_id):

        # generar una lista de ids con las ubicaciones internas
        locations = self.env['stock.location'].search([('usage', '=', 'internal')])
        ids = []
        for loc in locations:
            ids.append(loc.id)

        # buscar quants con ubicaciones internas y el producto que quiero
        quants = self.env['stock.quant'].search([
            ('location_id', 'in', ids),
            ('product_id', '=', product_id.id),
            ('reservation_id', '=', False),
        ])
        data = {}
        for quant in quants:
            loc_id = quant.location_id.location_id.name
            if loc_id not in data:
                data[loc_id] = int(quant.qty)
            else:
                data[loc_id] += int(quant.qty)

        return data

    @api.multi
    def calc_formated_stock(self, product_id):
        """
            formatear la informacion de sucursales y cantidades
        """
        data = self.calc_virtual_stock(product_id)
        ret = 'Sucursal --- Cantidad\n' if data else ''
        for loc in data:
            ret += u'{} ---> {} Un\n'.format(loc, data[loc])

        return ret
