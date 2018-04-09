# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.template"

    upv = fields.Integer(
        help='Agrupacion mayorista'
    )

    item_id = fields.Many2one(
        'product_autoload.item'
    )

    item_code = fields.Char(
        help="Code from bulonfer, not shown"
    )

    default_item_code = fields.Char(
        help="Code from bulonfer, extracted from default_code",
        calculated='_get_default_item_code'
    )

    wholesaler_bulk = fields.Integer(
        help="Bulk Wholesaler quantity of units",
    )

    retail_bulk = fields.Integer(
        help="Bulk retail quantity of units",
    )

    invalidate_category = fields.Boolean(
        help="Category needs rebuild"
    )

    @api.one
    @api.depends('default_code')
    def _get_default_item_code(self):
        return self.default_code.split('.')[0]
