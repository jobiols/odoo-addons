# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, models, fields


class Item(models.Model):
    _description = "Item related to each product"
    _name = 'product_autoload.item'

    name = fields.Char(
        help="Item name to show in category full name"
    )
    code = fields.Char(
        help="Code from bulonfer, not shown",
        select=1
    )
    origin = fields.Char(
        help="where the product was made"
    )
    section = fields.Char(
        help="Code from bulonfer, not shown"
    )
    family = fields.Char(
        help="Code from bulonfer, not shown"
    )
    margin = fields.Float(
        help="Profit margin suggested by the vendor for this item"
    )

    _sql_constraints = [
        ('uniq_code', 'unique(code)', "The item code must be unique !"),
    ]

    @api.multi
    @api.depends('margin')
    def change_margin(self):
        for item in self:
            # forzar recalculo de precios.
            prod_obj = self.env['product.template']
            prod = prod_obj.search([('item_code', '=', item.code)])
            if prod:
                print 'recalculando ', prod.default_code, item.margin
                prod.recalculate_list_price(item.margin)
