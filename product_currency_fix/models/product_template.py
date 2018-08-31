# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_product_price = fields.Float(
        digits_compute=dp.get_precision('Product Price'),
        groups="base.group_user",
        string="Product Cost",
        help="Purchase cost in the product currency."
    )
