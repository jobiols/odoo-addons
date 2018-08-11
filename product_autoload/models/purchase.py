# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount = fields.Float(
        string='Discount (%)',
        digits=dp.get_precision('Discount'),
        default=0.0
    )

    bprice = fields.Float(
        string='Bulonfer Price',
        digits=dp.get_precision('Product'),
        default=0.0
    )


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_calc(self):
        for purchase_order in self:
            ctx = dict(
                self._context,
                purchase_order_id=purchase_order.id
                )

            return {
                'name': _('Check Bulonfer prices'),
                'view_type': 'form',
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                'res_model': 'product_autoload.check_prices',
                'target': 'new',
                'context': ctx
            }
