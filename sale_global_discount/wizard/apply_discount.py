# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields, _


class ApplyDiscount(models.TransientModel):
    _name = "sale_global_discount.apply_discount"

    discount = fields.Float(
        help="Discount to apply to each SO line"
    )

    @api.multi
    def apply_discount(self):
        for rec in self:
            so_id = self._context['sale_order_id']
            sale_order_obj = self.env['sale.order']
            so = sale_order_obj.search([('id', '=', so_id)])
            for sol in so.order_line:
                sol.discount = rec.discount
