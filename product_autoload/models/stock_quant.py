# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import models, fields, api


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_tmpl_id = fields.Many2one(
        related="product_id.product_tmpl_id",
        store=True
    )
