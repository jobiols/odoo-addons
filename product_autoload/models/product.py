# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from mappers import ProductMapper, SectionMapper, ItemMapper, FamilyMapper, \
    ProductCodeMapper
import csv
from openerp.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = "product.template"

    upv = fields.Integer(
        help='Agrupacion mayorista'
    )

    item_id = fields.Many2one(
        'product_autoload.item'
    )

    productcode_ids = fields.One2many(
        'product_autoload.productcode',
        'product_id',
        help="All barcodes belonging to this product"
    )

    item_code = fields.Char(
        help="Code from bulonfer, not shown"
    )

    default_item_code = fields.Char(
        help="Code from bulonfer, extracted from default_code",
        calculated='_get_default_item_code'
    )

    wholesaler_bulk = fields.Integer(

    )

    retail_bulk = fields.Integer(

    )

    @api.one
    @api.depends('default_code')
    def _get_default_item_code(self):
        return self.default_code.split('.')[0]

    @api.multi
    def process_file(self, file_path, file, class_mapper, vendor=False,
                     supplierinfo=False):
        """ Procesa un archivo csv con un mapper
        """

        try:
            with open(file_path + file, 'r') as file_csv:
                reader = csv.reader(file_csv)
                for line in reader:
                    if line:
                        prod = class_mapper(line, file_path, vendor,
                                            supplierinfo)
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
        self.process_file(file_path, 'productcode.csv', ProductCodeMapper)
        item_obj.link_data()
        item_obj.create_categories()

    @api.model
    def auto_load(self, file_path):
        """ Carga todos los productos que tienen timestamp > ultima carga
        """
        self.send_email('Inicio de proceso',
                        'Hola, te aviso que inicio el proceso')
        bulonfer = self.env['res.partner'].search(
            [('name', 'like', 'Bulonfer')])
        if not bulonfer:
            raise Exception('Vendor Bulonfer not found')

        supplierinfo = self.env['product.supplierinfo']

        try:
            self.process_file(file_path, 'data.csv', ProductMapper,
                              vendor=bulonfer, supplierinfo=supplierinfo)
            self.category_load(file_path)
            self.send_email('Fin del proceso',
                            'Hola, te aviso que finalizo el proceso')

        except Exception as ex:
            _logger.error('Falla del proceso---------------------')
            self.send_email('Falla del proceso', ex.message)
            raise Exception('=== Falla del proceso === %s', ex.message)

    @api.model
    def send_email(self, subject, body):
        _logger.info('entra en send mail --------------------------------')
        mail_mail = self.env['mail.mail']
        user = self.env['res.users'].search([('id', '=', 1)])
        if not user.email:
            _logger.error(_('Email Required to notify load failure'))
            return False
        email_to = 'jorge.obiols@gmail.com'
        mail_ids = []

        mail_ids.append(mail_mail.create({
            'email_from': user.email,
            'email_to': email_to,
            'subject': subject,
            'body_html': '<pre>%s</pre>' % body}))

        # force direct delivery
        mail_mail.send(mail_ids)
        _logger.info('-------------->>>> mail sent.')
