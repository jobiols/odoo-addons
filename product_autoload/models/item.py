# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields


class Item(models.Model):
    """ El item se relaciona con el producto basado en el campo item_code
    """
    _name = 'product_autoload.item'

    item_code = fields.Char(
        help="Code from bulonfer, not shown"
    )
    name = fields.Char(
        help="Item name to show in category full name"
    )
    origin = fields.Char(
        help="where the product was made"
    )
    section_code = fields.Char(
        help="Code from bulonfer, not shown"
    )
    family_code = fields.Char(
        help="Code from bulonfer, not shown"
    )
    family_id = fields.Many2one(
        'product_autoload.family',
        help="family to which the item belongs"
    )
    section_id = fields.Many2one(
        'product_autoload.section',
        help='section to which the item belongs'
    )

    product_ids = fields.One2many(
        'product.product',
        'item_id',
        help="All products belonging to this item"
    )

    @api.model
    def unlink_data(self):

        # recorrer todos los productos y deslinkear las categorias
        for prod in self.env['product.template'].search([]):
            prod.categ_id = 1

        # eliminar los datos de las tres tablas
        for table in ['product_autoload.family',
                      'product_autoload.section',
                      'product_autoload.item']:
            for item in self.env[table].search([]):
                item.unlink()

    @api.model
    def link_data(self):
        item_obj = self.env['product_autoload.item']
        family_obj = self.env['product_autoload.family']
        section_obj = self.env['product_autoload.section']
        product_obj = self.env['product.product']

        # linkear todos los datos
        for item in item_obj.search([]):
            # Linkear item con familia.
            # Chequeo: El codigo family_code de item debe existir en
            # family.csv y debe ser unico.
            family = family_obj.search(
                [('family_code', '=', item.family_code)])
            if not family:
                raise Exception('Item %s points to family %s but no family '
                                'record found in family.csv', item.item_code,
                                item.family_code)
            try:
                family.ensure_one()
                item.family_id = family.id
                _logger.info('linked item %s with family %s', item.name,
                             family.name)
            except ValueError:
                raise Exception('Item %s points to family %s but multiple '
                                'records found in family.csv', item.item_code,
                                item.family_code)

            # Linkear con seccion
            # Chequeo: El codigo section_code de item debe existir en
            # section.csv y debe ser unico.
            section = section_obj.search(
                [('section_code', '=', item.section_code)])
            if not section:
                raise Exception('Item %s points to section %s but no section '
                                'record found in section.csv', item.item_code,
                                item.section_code)
            try:
                section.ensure_one()
                item.section_id = section.id
                _logger.info('linked item %s with section %s', item.name,
                             item.section_code)
            except ValueError:
                raise Exception('Item %s points to section %s but multiple '
                                'records found in section.csv', item.item_code,
                                item.section_code)

            # Linkear con productos
            # Chequeo: El codigo item_code de item debe existir en product
            product = product_obj.search(
                [('item_code', '=', item.item_code)]
            )
            if not product:
                raise Exception('Item points to product tagged with '
                                'idrubro=%s but no product found',
                                item.item_code)
            _logger.info('Linking %s products with item %s', len(product),
                         item.item_code)
            for prod in product:
                prod.item_id = item.id
                _logger.info('Linked product %s with item %s',
                             prod.default_code, item.item_code)

    @api.multi
    def get_category(self, item_code):

        categ_obj = self.env['product.category']
        item_obj = self.env['product_autoload.item']

        item = item_obj.search([('item_code', '=', item_code)])
        categ_id = categ_obj.search([('name', '=', item.name)])
        if not categ_id:
            categ_id = categ_obj.create({'name': item.name})

        if not categ_id.parent_id:
            parent = categ_obj.create({'name': item.family_id.name})
            categ_id.parent_id = parent

        return categ_id

    @api.multi
    def assign_category(self, prod):
        prod.categ_id = self.get_category(prod.item_code)
        _logger.info('setting category %s to product %s',
                     prod.categ_id.complete_name, prod.default_code)

    @api.multi
    def create_categories(self):
        product_obj = self.env['product.product']

        # recorrer todos los productos que tienen proveedor bulonfer y
        # asignarles una familia

        # TODO Arreglar esta porqueria
        for prod in product_obj.search([]):
            flag = False
            for vendor in prod.seller_ids:
                if vendor.name.name[0:8] == 'Bulonfer':
                    flag = True
            if flag:
                self.assign_category(prod)
