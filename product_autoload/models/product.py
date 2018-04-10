# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.template"

    item_code = fields.Char(
        help="Code from bulonfer, not shown",
        select=1
    )

    upv = fields.Integer(
        help='Agrupacion mayorista'
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

    @api.multi
    def recalculate_list_price(self, margin):
        for prod in self:
            prod.list_price = prod.standard_price * (1 + margin)
            _logger.info('{} {} <<< {}'.format(
                prod.default_code,
                prod.list_price,
                prod.standard_price))
