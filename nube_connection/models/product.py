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

    #######################################################################
    # Esto es lo que calcula el virtual available, se le agrega codigo para
    # la replicacion al final
    # No pude hacer funcionar el super, por problemas con el api viejas asi
    # que tuve que copiar el metodo completo y agregarle el codigo al final
    #######################################################################
    def _product_available(self, cr, uid, ids, field_names=None, arg=False, context=None):
        context = context or {}
        field_names = field_names or []

        domain_products = [('product_id', 'in', ids)]
        domain_quant, domain_move_in, domain_move_out = [], [], []
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations(cr, uid, ids, context=context)
        domain_move_in += self._get_domain_dates(cr, uid, ids, context=context) + [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_products
        domain_move_out += self._get_domain_dates(cr, uid, ids, context=context) + [('state', 'not in', ('done', 'cancel', 'draft'))] + domain_products
        domain_quant += domain_products

        if context.get('lot_id'):
            domain_quant.append(('lot_id', '=', context['lot_id']))
        if context.get('owner_id'):
            domain_quant.append(('owner_id', '=', context['owner_id']))
            owner_domain = ('restrict_partner_id', '=', context['owner_id'])
            domain_move_in.append(owner_domain)
            domain_move_out.append(owner_domain)
        if context.get('package_id'):
            domain_quant.append(('package_id', '=', context['package_id']))

        domain_move_in += domain_move_in_loc
        domain_move_out += domain_move_out_loc
        moves_in = self.pool.get('stock.move').read_group(cr, uid, domain_move_in, ['product_id', 'product_qty'], ['product_id'], context=context)
        moves_out = self.pool.get('stock.move').read_group(cr, uid, domain_move_out, ['product_id', 'product_qty'], ['product_id'], context=context)

        domain_quant += domain_quant_loc
        quants = self.pool.get('stock.quant').read_group(cr, uid, domain_quant, ['product_id', 'qty'], ['product_id'], context=context)
        quants = dict(map(lambda x: (x['product_id'][0], x['qty']), quants))

        moves_in = dict(map(lambda x: (x['product_id'][0], x['product_qty']), moves_in))
        moves_out = dict(map(lambda x: (x['product_id'][0], x['product_qty']), moves_out))
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            id = product.id
            qty_available = float_round(quants.get(id, 0.0), precision_rounding=product.uom_id.rounding)
            incoming_qty = float_round(moves_in.get(id, 0.0), precision_rounding=product.uom_id.rounding)
            outgoing_qty = float_round(moves_out.get(id, 0.0), precision_rounding=product.uom_id.rounding)
            virtual_available = float_round(quants.get(id, 0.0) + moves_in.get(id, 0.0) - moves_out.get(id, 0.0), precision_rounding=product.uom_id.rounding)
            res[id] = {
                'qty_available': qty_available,
                'incoming_qty': incoming_qty,
                'outgoing_qty': outgoing_qty,
                'virtual_available': virtual_available,
            }

        # la parte de arriba es copia textual del metodo original
        # luego, si el record tiene el do_published lo registro para replicar
        prod_obj = self.pool.get('product.product')
        replication = self.pool.get('nube.replication')
        prods = prod_obj.browse(cr, uid, ids)
        for prod in prods:
            if prod.do_published:
                replication.new_record(cr, uid, ids, self._name, prod.id)

        return res

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

    @api.multi
    def write(self, vals):
        """ Registrar el registro para replicar si corresponde
        """
        if self.do_published:
            replication = self.env['nube.replication']
            replication.new_record(self._name, self.id)
        ret = super(ProductProduct, self).write(vals)
        return ret
