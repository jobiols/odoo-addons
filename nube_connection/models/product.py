# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import markdown
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    woo_categ = fields.Many2one(
        'curso.woo.categ',
        'Categoría Tienda Nube',
        help=u'Categoría Tienda Nube'
    )

    nube_id = fields.Integer(
        help=u'Identifica el producto en tienda nube'
    )

    published = fields.Boolean(
        'Publicado en tienda nube',
        help=u'Indica si se publica en tienda nube'
    )
    promotional_price = fields.Float(
        'Precio Promocional',
        digits=(16, 2),
        help=u'Precio promocional para tienda nube, si se pone un precio aca"'
             u'aparece como promocion, con precio publico tachado'
    )
