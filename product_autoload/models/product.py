# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from mappers import ProductMapper, SectionMapper, ItemMapper, FamilyMapper
import csv


class ProductProduct(models.Model):
    _inherit = "product.product"

    item_id = fields.Many2one(
        'product_autoload.item'
    )

    item_code = fields.Char(
        help="Code from bulonfer, not shown"
    )

    @api.multi
    def process_file(self, file_path, file, class_mapper, vendor=False,
                     supplierinfo=False):
        """ Procesa un archivo csv con un mapper
        """
        try:
            with open(file_path + file, 'r') as file_csv:
                reader = csv.reader(file_csv)
                for line in reader:
                    prod = class_mapper(line, file_path, vendor, supplierinfo)
                    prod.execute(self.env)
        except IOError as ex:
            _logger.error('%s %s', ex.filename, ex.strerror)

    @api.model
    def category_load(self, file_path):
        """ Carga las tablas auxiliares por unica vez, o cuando haga falta
        """

        item_obj = self.env['product_autoload.item']
        item_obj.unlink_data()
        self.process_file(file_path, 'section.csv', SectionMapper)
        self.process_file(file_path, 'family.csv', FamilyMapper)
        self.process_file(file_path, 'item.csv', ItemMapper)
        item_obj.link_data()
        item_obj.create_categories()

    @api.model
    def auto_load(self, file_path):
        """ Carga todos los productos que tienen timestamp > ultima carga
        """
        bulonfer = self.env['res.partner'].search(
            [('name', 'like', 'Bulonfer')])
        supplierinfo = self.env['product.supplierinfo']
        self.process_file(file_path, 'data.csv', ProductMapper,
                          vendor=bulonfer, supplierinfo=supplierinfo)

        self.category_load(file_path)
