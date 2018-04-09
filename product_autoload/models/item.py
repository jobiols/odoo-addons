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
