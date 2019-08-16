# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root


from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        ret = super(SaleOrderLine, self).product_id_change()

        if self.product_id.customer_ids:
            si_obj = self.env['product.customerinfo']
            cust_info = si_obj.search([
                ('name', '=', self.order_id.partner_id.id),
                ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)])

            self.name = '[{}] {}'.format(cust_info.product_code,
                                         cust_info.product_name)

        return ret
