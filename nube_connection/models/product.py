# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields, api
from openerp.tools.float_utils import float_round
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
             '- Esta tildado para publicacion \n'
             '- Tiene una foto\n'
             '- Tiene descripcion\n'
             '- Tiene categorias nube\n'
             '- Estado es Normal',
        compute='_compute_do_published',
        readonly=True,
        store=True,
    )
    promotional_price = fields.Float(
        'Precio Promocional',
        digits=(16, 2),
        help=u'Precio promocional para tienda nube, si se pone un precio aca '
             u'aparece como promocion, con precio publico tachado.'
    )
    virtual_stock = fields.Integer(
        help='Campo tecnico para almacenar el ultimo valor del stock virtual'
    )

    @api.model
    def compute_delta_stock(self):
        """ Este metodo se ejecuta desde el script odoorpc para marcar los
            productos que tienen stock modificado, al modificar el virtual_stock
            aparecen en nube_replication
        """
        prods = self.search([('do_published', '=', True)])
        _logger.info('Revisando %s productos por stock' % len(prods))
        for rec in prods:
            if rec.virtual_stock != rec.virtual_available:
                rec.virtual_stock = rec.virtual_available
                name = rec.default_code or rec.name or '???'
                _logger.info('Marcando producto ' + name)
        return True

    @api.multi
    @api.depends('published', 'image_medium', 'description', 'woo_categ_ids',
                 'active', 'state')
    def _compute_do_published(self):
        for ret in self:
            ret.do_published = \
                ret.published and \
                ret.image_medium and \
                ret.description and \
                ret.woo_categ_ids and \
                ret.active and \
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

    @api.model
    def create(self, vals):
        ret = super(ProductProduct, self).create(vals)
        self.new_replication(ret.id)
        return ret

    @api.multi
    def write(self, vals):
        ret = super(ProductProduct, self).write(vals)
        if self.do_published:
            self.new_replication(self.id)
        return ret

    def new_replication(self, id_product):
        """ Crear el registro de replicacion
        """
        replication = self.env['nube.replication']
        replication.new_record(id_product)
