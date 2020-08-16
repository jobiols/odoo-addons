# Copyright 2020 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class Product(models.Model):
    _inherit = "product.template"

    tag_ids = fields.Many2many(
        'product.tag',
        column1='product_id',
        column2='tag_ids',
        help='Classify or analyze your products with tags.')


