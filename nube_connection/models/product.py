# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


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
        string='Publicar en tienda nube',
        help=u'Al tildarlo se permite la publicacion en la tienda'
    )
    do_published = fields.Boolean(
        string='Verificacion de publicado',
        help='Indica si se publica realmente, y es verdadero si comple con:\n'
             'Esta tildado para publicacion \n'
             'Tiene una foto\n'
             'Tiene descripcion\n'
             'Tiene categorias nube\n'
             'Estado es Normal',
        compute='_compute_do_published',
        readonly=True,
        store=True
    )
    promotional_price = fields.Float(
        'Precio Promocional',
        digits=(16, 2),
        help=u'Precio promocional para tienda nube, si se pone un precio aca '
             u'aparece como promocion, con precio publico tachado.'
    )
    witness_quantity = fields.Float(
        help='Cantidad de producto testigo, cuando se hace una subida a la '
             'nube se verifica si cambio y si es asi se sube el producto.'
    )
    stock_match = fields.Boolean(
        help='indica que el stock virtual y el que se chequeo la ultima vez '
             'son iguales',
        compute='_compute_stock_match',
        store=True
    )

    @api.multi
    @api.depends('witness_quantity', 'virtual_available')
    def _compute_stock_match(self):
        for rec in self:
            match = rec.witness_quantity == rec.virtual_available
            rec.stock_match = match

    @api.model
    def prepare_nube_upload(self):
        """ Prepara el upload revisando los registros que tienen
            witness_quantity distinto de virtual_available, si es asi los
            igualan y le actualizan write_date a now
        """
        _logger.info('Prepare Nube Uplad')

        product_obj = self.env['product.product']
        to_prepare = product_obj.search([('stock_match', '=', False)],
                                        limit=100)
        now = fields.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for rec in to_prepare:
            _logger.info('%s qty=%s' % (rec.default_code,
                                        rec.virtual_available))
            rec.write({
                'write_date': now,
                'witness_quantity': rec.virtual_available
            })
        return len(to_prepare)

    @api.multi
    @api.depends('published', 'image_medium', 'description', 'woo_categ_ids',
                 'state')
    def _compute_do_published(self):
        for ret in self:
            ret.do_published = \
                ret.published and \
                ret.image_medium and \
                ret.description and \
                ret.woo_categ_ids and \
                ret.state == 'sellable'

    @api.multi
    def copy(self, default=None):
        self.ensure_one()

        if default is None:
            default = {}

        default['nube_id'] = 0
        return super(ProductProduct, self).copy(default=default)

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
