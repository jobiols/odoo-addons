# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from mappers import ProductMapper, SectionMapper, ItemMapper, FamilyMapper, \
    ProductCodeMapper
import csv
from time import time
from datetime import datetime, timedelta


class ProductProduct(models.Model):
    _inherit = "product.template"

    upv = fields.Integer(
        help='Agrupacion mayorista'
    )

    item_id = fields.Many2one(
        'product_autoload.item'
    )

    item_code = fields.Char(
        help="Code from bulonfer, not shown"
    )

    default_item_code = fields.Char(
        help="Code from bulonfer, extracted from default_code",
        calculated='_get_default_item_code'
    )

    wholesaler_bulk = fields.Integer(
        help="Bulk Wholesaler quantity of units",
    )

    retail_bulk = fields.Integer(
        help="Bulk retail quantity of units",
    )

    @api.one
    @api.depends('default_code')
    def _get_default_item_code(self):
        return self.default_code.split('.')[0]

    @api.multi
    def process_file(self, file_path, file, class_mapper, vendor=False,
                     supplierinfo=False):
        """ Procesa un archivo csv con un mapper teniendo en cuenta la fecha
            de los registros
        """
        last_replication = self.env['ir.config_parameter'].get_param(
            'last_replication', '')
        check_date = self.env['ir.config_parameter'].get_param(
            'import_only_new', '')

        try:
            with open(file_path + file, 'r') as file_csv:
                reader = csv.reader(file_csv)
                for line in reader:
                    if line:
                        obj = class_mapper(line, file_path, vendor,
                                           supplierinfo)
                        if not check_date:
                            if obj.write_date > last_replication:
                                obj.execute(self.env)
                            else:
                                obj.execute(self.env)

            self.env['ir.config_parameter'].set_param('last_replication',
                                                      str(datetime.now()))
        except IOError as ex:
            _logger.error('{} {}'.format(ex.filename, ex.strerror))

    @api.model
    def category_load(self, file_path):
        """ Carga las tablas auxiliares por unica vez, o cuando haga falta
        """
        item_obj = self.env['product_autoload.item']
        item_obj.unlink_data()
        self.process_file(file_path, 'section.csv', SectionMapper)
        self.process_file(file_path, 'family.csv', FamilyMapper)
        self.process_file(file_path, 'item.csv', ItemMapper)
        self.process_file(file_path, 'productcode.csv', ProductCodeMapper)
        item_obj.link_data()
        item_obj.create_categories()

    @api.model
    def auto_load(self, file_path):
        """ Actualiza los productos
        """
        self.send_email('Replicacion Bulonfer, Inicio', 'Se inicio el proceso')
        start_time = time()

        bulonfer = self.env['res.partner'].search(
            [('name', 'like', 'Bulonfer')])
        if not bulonfer:
            raise Exception('Vendor Bulonfer not found')
        supplierinfo = self.env['product.supplierinfo']

        try:
            self.process_file(file_path, 'data.csv', ProductMapper,
                              vendor=bulonfer, supplierinfo=supplierinfo)
            self.category_load(file_path)
            elapsed_time = time() - start_time
            self.send_email('Replicacion Bulonfer, Fin', 'Termino el proceso',
                            elapsed_time)

        except Exception as ex:
            self.send_email('Replicacion Bulonfer ERROR', ex.message)
            raise Exception('=== Falla del proceso === {}'.format(ex.message))

