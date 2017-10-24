# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from openerp import SUPERUSER_ID
from openerp.exceptions import Warning
from lxml import etree


class ProductProduct(models.Model):
    _inherit = 'product.product'

    prod_in_box = fields.Float(
            u'Cant producto por caja',
            help=u'Cantidad de metros cuadrados o lineales que entran en una caja'
    )
    prod_in_box_uom = fields.Selection([
        ('na', 'No aplica'),
        ('mt2', 'mts cuadrados'),
        ('mt', 'mts'),
    ],
            'Unidad', required=True,
            default='mt2'
    )
    price_1 = fields.Float(
            u'Precio 1',
            compute='_compute_prices'
    )
    price_2 = fields.Float(
            u'Precio 2',
            compute='_compute_prices'
    )
    price_3 = fields.Float(
            u'Precio 3',
            compute='_compute_prices'
    )

    @api.one
    @api.constrains('prod_in_box', 'prod_in_box_uom', 'type')
    def _check_prod_in_box(self):
        if self.prod_in_box_uom == 'na' and self.prod_in_box - 0.0 > 0.001:
            raise Warning('Cantidad de producto por caja debe ser cero')

        if self.prod_in_box_uom != 'na' and self.type != 'product':
            raise Warning('Si aplica cantidad de producto por caja, '
                          'el tipo de producto debe ser almacenable')

    def _get_pricelists(self):
        """ traer las tres listas de precio de la configuracion
        """
        lists = self.env['prices.config.settings'].sudo().default_get('')

        pricelist = self.env['product.pricelist']
        pl_ids = []
        for ix in range(0, 3):
            pl_ids.append(pricelist.search([('id', '=', lists['pricelist_{}'.format(ix + 1)])]))

        #import wdb;wdb.set_trace()

        # TODO arreglar esto, estamos forzando las listas de precio
        price = self.env['product.pricelist']
        pl_ids[0] = price.search([('id', '=', 6)])   # 1=reves 6=suelos
        pl_ids[1] = price.search([('id', '=', 3)])
        pl_ids[2] = price.search([('id', '=', 0)])

        return pl_ids

    @api.one
    @api.depends('standard_price')
    def _compute_prices(self):

        # traer las pricelist configuradas
        pl_ids = self._get_pricelists()

        #import wdb;wdb.set_trace()
        # actualizar los precios de los campos solo si las listas de precio no son False
        # no logre hacer esto con la api 8, queda con la api 7
        if pl_ids[0]:
            self.price_1 = self.pool.get('product.pricelist').price_get(
                    self.env.cr, SUPERUSER_ID, [pl_ids[0].id], self.id, 1.0,
                    context=None)[pl_ids[0].id]

        if pl_ids[1]:
            self.price_2 = self.pool.get('product.pricelist').price_get(
                    self.env.cr, SUPERUSER_ID, [pl_ids[1].id], self.id, 1.0,
                    context=None)[pl_ids[1].id]

        if pl_ids[2]:
            self.price_3 = self.pool.get('product.pricelist').price_get(
                    self.env.cr, SUPERUSER_ID, [pl_ids[2].id], self.id, 1.0,
                    context=None)[pl_ids[2].id]

    @api.model
    def fields_view_get(self, view_id=None, view_type='tree', context=None, toolbar=False, submenu=False):
        """ Sobreescribimos fields_view_get para cambiar los nombres de los campos del tree view
        """
        result = super(ProductProduct, self).fields_view_get(
                view_id=view_id,
                view_type=view_type,
                toolbar=toolbar,
                submenu=submenu)

        if view_type == 'tree':

            # traer las pricelist configuradas
            pl_ids = self._get_pricelists()

            doc = etree.XML(result['arch'])
            for ix in range(0, 3):
                for node in doc.xpath("//field[@name='price_{}']".format(ix + 1)):
                    if pl_ids[ix]:
                        node.set('string', pl_ids[ix].name)
                        if pl_ids[ix].restricted:
                            node.set('groups', 'base.group_erp_manager,reves_default.group_reves_admin_users')
                    else:
                        node.set('invisible', '1')
                        node.set('modifiers', '{"readonly": true, "tree_invisible": true}')

            result['arch'] = etree.tostring(doc)

        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
