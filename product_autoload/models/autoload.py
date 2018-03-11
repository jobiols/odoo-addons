# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from time import time
from datetime import datetime, timedelta
import csv
from mappers import MAP_WRITE_DATE
from openerp import api, models, fields
from mappers import ProductMapper

_logger = logging.getLogger(__name__)

SECTION = 'section.csv'
FAMILY = 'family.csv'
ITEM = 'item.csv'
DATA = 'data.csv'
PRODUCTCODE = 'productcode.csv'

IM_CODE = 0
IM_NAME = 1
IM_ORIGIN = 2
IM_SECTION_CODE = 3
IM_FAMILY_CODE = 4
IM_LEN = 5

PC_BARCODE = 0
PC_PRODUCT_CODE = 1
PC_UXB = 2
PC_LEN = 3


class AutoloadMgr(models.Model):
    _name = 'product_autoload.manager'
    _description = "Manage product data import"

    name = fields.Char()

    @staticmethod
    def load_section(data_path):
        res = dict()
        with open(data_path + SECTION, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                _logger.info('loading section {}'.format(line[1]))
                res[line[0]] = line[1]
        return res

    @staticmethod
    def load_family(data_path):
        res = dict()
        with open(data_path + FAMILY, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                _logger.info('loading family {}'.format(line[1]))
                res[line[0]] = line[1]
        return res

    @api.model
    def load_item(self, data_path):
        item_obj = self.env['product_autoload.item']
        item_obj.search([]).unlink()
        with open(data_path + ITEM, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                _logger.info('loading item {}'.format(line[IM_NAME]))
                values = {
                    'code': line[IM_CODE].strip(),
                    'name': line[IM_NAME].strip(),
                    'origin': line[IM_CODE].strip(),
                    'section': self._section[line[IM_SECTION_CODE]].strip(),
                    'family': self._family[line[IM_FAMILY_CODE]].strip()
                }
                item_obj.create(values)

    @api.model
    def load_productcode(self, data_path):
        item_obj = self.env['product_autoload.productcode']
        item_obj.search([]).unlink()
        count = 0
        with open(data_path + PRODUCTCODE, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                count += 1
                if count == 2000:
                    count = 0
                    _logger.info('loading +2000 barcodes')
                values = {
                    'barcode': line[PC_BARCODE].strip(),
                    'product_code': line[PC_PRODUCT_CODE].strip(),
                    'uxb': line[PC_UXB].strip(),
                }
                item_obj.create(values)

    @api.model
    def load_product(self, data_path):
        """ Carga todos los productos teniendo en cuenta la fecha
        """
        last_replication = self.env['ir.config_parameter'].get_param(
            'last_replication', '')
        import_only_new = self.env['ir.config_parameter'].get_param(
            'import_only_new', True)

        model_data_obj = self.env['ir.model.data']
        res_model, none_categ_id = model_data_obj.get_object_reference(
            'product_autoload', 'bulonfer_none_categ')

        bulonfer = self.env['res.partner'].search(
            [('name', 'like', 'Bulonfer')])
        if not bulonfer:
            raise Exception('Vendor Bulonfer not found')

        supplierinfo = self.env['product.supplierinfo']
        self.prod_processed = 0
        with open(data_path + DATA, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                if line and \
                    (import_only_new or
                             line[MAP_WRITE_DATE] > last_replication
                     ):
                    obj = ProductMapper(line, data_path, bulonfer,
                                        supplierinfo)
                    obj.execute(self.env, none_categ_id)
                    self.prod_processed += 1

    @api.model
    def run(self, send_mail=True):
        """ Actualiza todos los productos
        """
        start_time = time()
        data_path = self.env['ir.config_parameter'].get_param(
            'data_path', '')
        email_from = self.env['ir.config_parameter'].get_param(
            'email_from', '')
        email_to = self.env['ir.config_parameter'].get_param(
            'email_notification', '')

        try:
            rec = self.create({'name': 'Inicia Proceso'})
            if send_mail:
                self.send_email('Replicacion Bulonfer #{}, '
                                'Inicio'.format(rec.id),
                                'Se inicio el proceso',
                                email_from, email_to)

            self._section = self.load_section(data_path)
            self._family = self.load_family(data_path)

            self.load_item(data_path)
            self.load_productcode(data_path)
            self.load_product(data_path)

            elapsed_time = time() - start_time

            self.create({'name': 'Termina Proceso'})

            if send_mail:
                self.send_email('Replicacion Bulonfer #{}, '
                                'Fin'.format(rec.id),
                                self.get_stats(elapsed_time),
                                email_from, email_to)

            self.env['ir.config_parameter'].set_param('last_replication',
                                                      str(datetime.now()))
        except Exception as ex:
            self.send_email('Replicacion Bulonfer #{}, '
                            'ERROR'.format(rec.id), ex.message,
                            email_from, email_to)
            _logger.error('Replicacion Bulonfer {}'.format(ex.message))
            raise

    @api.model
    def update_categories(self):
        # linkear las categorias
        categ_obj = self.env['product.category']
        item_obj = self.env['product_autoload.item']
        model_data_obj = self.env['ir.model.data']
        res_model, none_categ_id = model_data_obj.get_object_reference(
            'product_autoload', 'bulonfer_none_categ')
        email_from = self.env['ir.config_parameter'].get_param('email_from',
                                                               '')
        email_to = self.env['ir.config_parameter'].get_param(
            'email_notification', '')

        prods = self.env['product.template'].search(
            [('categ_id', '=', none_categ_id)], limit=1000)
        for prod in prods:
            # buscar el item que corresponde al producto
            item = item_obj.search([('code', '=', prod.item_code)])
            if not item:
                text = 'product {} has item = {} but there is no such item ' \
                       'in item.csv'.format(prod.default_code, prod.item_code)
                self.send_email('Replicacion Bulonfer, ERROR', text,
                                email_from, email_to)
                raise Exception(text)

            # buscar seccion o crearla
            sec_id = categ_obj.search([('name', '=', item.section)])
            if not sec_id:
                sec_id = categ_obj.create({'name': item.section})

            # buscar seccion / familia o crearla
            sec_fam_id = categ_obj.search([('name', '=', item.family),
                                           ('parent_id.name', '=',
                                            item.section)])
            if not sec_fam_id:
                sec_fam_id = categ_obj.create({'name': item.family,
                                               'parent_id': sec_id.id})

            # buscar seccion / familia / item o crearla
            categ_id = categ_obj.search([('name', '=', item.name),
                                         ('parent_id.name', '=', item.family),
                                         ('parent_id.parent_id.name', '=',
                                          item.section)])
            if not categ_id:
                categ_id = categ_obj.create({'name': item.name,
                                             'parent_id': sec_fam_id.id})
            _logger.info('Setting category {}'.format(categ_id.complete_name))
            prod.categ_id = categ_id

    @api.model
    def send_email(self, subject, body, email_from, email_to):
        email_to = email_to.split(',')
        # email_to = ['jorge.obiols@gmail.com', 'sagomez@gmail.com']
        smtp = self.env['ir.mail_server']
        message = smtp.build_email(email_from, email_to, subject, body)
        smtp.send_email(message)

    @api.model
    def get_stats(self, elapsed_time):
        elapsed = str(timedelta(seconds=elapsed_time))

        ret = u'Terminó el proceso\n'
        ret += u'Duración: {}\n'.format(elapsed)
        ret += u'Productos procesados: {}'.format(self.prod_processed)
        return ret
