# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp.osv import fields, osv


class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'

    def _get_route_selection(self, cr, uid, context=None):
        product_obj = self.pool.get('product.product')
        ctx = {}
        for dd in context:
            ctx[dd] = context[dd]

        data = []
        for loc in [u'AM', u'CH', u'GA', u'PA', u'SM']:
            ctx['location'] = loc
            prod = product_obj.browse(cr, uid, [14882], ctx)
            stk = prod._product_available()
            qty = stk[prod.id]
            if qty['virtual_available'] != 0.0:
                data.append(
                    (
                        loc,
                        '{} {}'.format(loc, int(qty['virtual_available']))
                    )
                )

        return data

    _columns = {
        'route_select': fields.selection(
            _get_route_selection,
            required=True),

    }
