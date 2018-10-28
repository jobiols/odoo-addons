# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import models, fields


class Error(models.Model):
    _description = "Errors from product uploads"
    _name = 'product_upload.error'

    log_id = fields.Integer(
    )

    name = fields.Char(

    )
