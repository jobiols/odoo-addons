# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

import markdown
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    woo_categ_ids = fields.Many2many(
        comodel_name='curso.woo.categ',
        string='Categorías Tienda Nube',
        help=u'Categorías Tienda Nube'
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

    @api.multi
    def get_woo_categs(self):
        """ Obtiene las categorias tienda nube de este producto esto se accede
            por xmlrpc al subir el producto a la tienda
        """
        for prod in self:
            ret = []
            for wc in prod.woo_categ_ids:
                ret.append(wc.nube_id)

        return ret