# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class ProductCode(models.Model):
    """ Contiene los codigos de barra de los productos
    """
    _name = 'product_autoload.productcode'

    barcode = fields.Char(
        help="Barcode not EIAN"
    )

    product_code = fields.Char(
        help="product default code",
        select=1
    )

    uxb = fields.Integer(
        help="unidades por bulto"
    )

#    _sql_constraints = [(
#        'uniq_barcode', 'unique(barcode)', "The barcode must be unique !"
#    )]
