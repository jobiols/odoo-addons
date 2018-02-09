# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class Barcode(models.Model):
    """ Pueden haber varios codigos de barra para un producto
    """
    _name = 'product_autoload.barcode'

    product_id = fields.Many2one(
        'product.product',
        help="product code"
    )

    barcode = fields.Char(
        help="Barcode"
    )

    _sql_constraints = [
        ('uniq_barcode', 'unique(barcode)', "The barcode must be unique !"),
    ]