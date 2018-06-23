# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    meli_code = fields.Char(
        string='Meli Publishing Code'
    )
