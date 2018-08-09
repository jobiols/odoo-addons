# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def apply_discount(self):
        for line in self:

            ctx = dict(
                self._context,
                sale_order_id=line.id
                )

            return {
                'name': _('Apply discount to all SO lines'),
                'view_type': 'form',
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                'res_model': 'sale_global_discount.apply_discount',
                'target': 'new',
                'context': ctx
            }
