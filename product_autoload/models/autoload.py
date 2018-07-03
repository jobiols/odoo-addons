# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import time
from datetime import datetime
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
IM_MARGIN = 5
IM_LEN = 6

PC_BARCODE = 0
PC_PRODUCT_CODE = 1
PC_UXB = 2
PC_LEN = 3


class AutoloadMgr(models.Model):
    _name = 'product_autoload.manager'
    _description = "Manage product data import"
    _order = 'id desc'

    name = fields.Char(

    )
    start_time = fields.Datetime(

    )
    elapsed_time = fields.Char(

    )
    statistics = fields.Html(

    )
    processed = fields.Integer(
        string="Processed products"
    )

    @staticmethod
    def load_section(data_path):
        """ Carga la estructura de datos en memoria
        """
        _logger.info('REPLICATION: loading sections')
        res = dict()
        with open(data_path + SECTION, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                res[line[0]] = line[1]
        return res

    @staticmethod
    def load_family(data_path):
        """ Carga la estructura de datos en memoria
        """
        _logger.info('REPLICATION: loading families')
        res = dict()
        with open(data_path + FAMILY, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                res[line[0]] = line[1]
        return res

    def load_item(self, data_path, item=ITEM):
        """ Carga los datos en un modelo, chequeando por modificaciones
            Si cambio el margen recalcula todos precios de los productos
        """
        prod_obj = self.env['product.template']
        item_obj = self.env['product_autoload.item']
        _logger.info('REPLICATION: loading items')

        with open(data_path + item, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                values = {
                    'code': line[IM_CODE].strip(),
                    'name': line[IM_NAME].strip(),
                    'origin': line[IM_CODE].strip(),
                    'section': self._section[line[IM_SECTION_CODE]].strip(),
                    'family': self._family[line[IM_FAMILY_CODE]].strip(),
                    'margin': line[IM_MARGIN].strip()
                }
                # buscar el codigo en la tabla
                item = item_obj.search([('code', '=', values['code'])])
                if item:
                    if not (item.origin == values['origin'] and
                            item.name == values['name'] and
                            item.section == values['section'] and
                            item.family == values['family'] and
                            item.margin == float(values['margin'])):
                        item.write(values)

                        # forzar recalculo de precios.
                        domain = [('item_code', '=', values['code'])]
                        prod = prod_obj.search(domain)
                        if prod:
                            prod.recalculate_list_price(item.margin)
                else:
                    item_obj.create(values)

                    # forzar recalculo de precios
                    domain = [('item_code', '=', values['code'])]
                    prod = prod_obj.search(domain)
                    if prod:
                        prod.recalculate_list_price(item.margin)

    def load_productcode(self, data_path, productcode):
        """ Borra la tabla productcode y la vuelve a crear con los datos nuevos
        """
        item_obj = self.env['product_autoload.productcode']
        item_obj.search([]).unlink()
        count = 0
        with open(data_path + productcode, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                count += 1
                if count == 4000:
                    count = 0
                    _logger.info('REPLICATION: loading +4000 barcodes')
                values = {
                    'barcode': line[PC_BARCODE].strip(),
                    'product_code': line[PC_PRODUCT_CODE].strip(),
                    'uxb': line[PC_UXB].strip(),
                }
                item_obj.create(values)

    def load_product(self, data_path):
        """ Carga todos los productos teniendo en cuenta la fecha
        """
        bulonfer = self.env['res.partner'].search([('ref', '=', 'BULONFER')])
        if not bulonfer:
            raise Exception('Vendor Bulonfer not found')

        last_replication = self.last_replication
        _logger.info('REPLICATION: Load products '
                     'with timestamp > {}'.format(last_replication))

        supplierinfo = self.env['product.supplierinfo']
        self.prod_processed = 0
        with open(data_path + DATA, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                if line and line[MAP_WRITE_DATE] > last_replication:
                    obj = ProductMapper(line, data_path, bulonfer,
                                        supplierinfo)
                    obj.execute(self.env)
                    self.prod_processed += 1

    @api.model
    def run(self, item=ITEM, productcode=PRODUCTCODE):
        """ Actualiza todos los productos.
        """
        # empezamos a contar el tiempo de proceso
        start_time = time.time()
        data_path = self.data_path

        rec = self.create({})
        _logger.info('REPLICATION: Start #{}'.format(rec.id))
        try:
            # Cargar en memoria las tablas chicas
            self._section = self.load_section(data_path)
            self._family = self.load_family(data_path)
            self.prod_processed = 0

            _logger.info('REPLICATION: Load disk tables')
            # Cargar en bd las demas tablas
            self.load_item(data_path, item)
            self.load_productcode(data_path, productcode)

            # Aca carga solo los productos que tienen fecha de modificacion
            # posterior a la fecha de proceso y los actualiza o los crea segun
            # sea necesario
            self.load_product(data_path)

            # terminamos de contar el tiempo de proceso
            elapsed_time = time.time() - start_time
            start = time.strftime('%Y-%m-%d %H:%M', time.localtime(start_time))
            elapsed = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            self.send_email('Replicacion Bulonfer #{}'.format(rec.id),
                            self.get_stats(start, elapsed),
                            self.email_from, self.email_to)

            self.last_replication = str(datetime.now())
            _logger.info('REPLICATION: End')

            rec.write({
                'name': 'Replicacion #{}'.format(rec.id),
                'start_time': start,
                'elapsed_time': elapsed,
                'statistics': self.get_stats(start, elapsed),
                'processed': self.prod_processed
            })

        except Exception as ex:
            _logger.error('Replicacion Bulonfer {}'.format(ex.message))
            self.send_email('Replicacion Bulonfer #{}, '
                            'ERROR'.format(rec.id), ex.message,
                            self.email_from, self.email_to)
            raise

    @api.model
    def update_categories(self):
        # linkear las categorias
        _logger.info('update categories')
        categ_obj = self.env['product.category']
        item_obj = self.env['product_autoload.item']
        prods = self.env['product.template'].search(
            [('invalidate_category', '=', True)], limit=400)
        for prod in prods:
            # buscar el item que corresponde al producto
            item = item_obj.search([('code', '=', prod.item_code)])
            if not item:
                text = 'product {} has item = {} but there is no such item ' \
                       'in item.csv'.format(prod.default_code, prod.item_code)
                self.send_email('Replicacion Bulonfer, ERROR', text,
                                self.email_from, self.email_to)
                raise Exception(text)

            # calcular el precio de lista
            prod.recalculate_list_price(item.margin)

            # buscar seccion o crearla en categorias
            sec_id = categ_obj.search([('name', '=', item.section),
                                       ('parent_id', '=', False)])
            if not sec_id:
                sec_id = categ_obj.create({'name': item.section,
                                           'property_cost_method': 'real',
                                           'removal_strategy_id': 1})

            # buscar seccion / familia o crearla
            sec_fam_id = categ_obj.search([('name', '=', item.family),
                                           ('parent_id.name', '=',
                                            item.section)])
            if not sec_fam_id:
                sec_fam_id = categ_obj.create({'name': item.family,
                                               'parent_id': sec_id.id,
                                               'property_cost_method': 'real',
                                               'removal_strategy_id': 1})

            # buscar seccion / familia / item o crearla
            categ_id = categ_obj.search([('name', '=', item.name),
                                         ('parent_id.name', '=', item.family),
                                         ('parent_id.parent_id.name', '=',
                                          item.section)])
            if not categ_id:
                categ_id = categ_obj.create({'name': item.name,
                                             'parent_id': sec_fam_id.id,
                                             'property_cost_method': 'real',
                                             'removal_strategy_id': 1})

            _logger.info('Setting %s --> %s' %
                         (prod.default_code, categ_id.complete_name))
            prod.write(
                {
                    'categ_id': categ_id.id,
                    'invalidate_category': False
                }
            )

    @api.multi
    def send_email(self, subject, body, email_from, email_to):
        email_to = email_to.split(',')
        if len(email_to) == 0:
            _logger.error('No hay destinatario de mail')
            return

        smtp = self.env['ir.mail_server']
        try:
            message = smtp.build_email(email_from, email_to, subject, body)
            smtp.send_email(message)
        except Exception as ex:
            _logger.error('Falla envio de mail %s' % ex.message)

    @api.multi
    def get_stats(self, start, elapsed):
        ret = u'Inicio: {}\n'.format(start)
        ret = u'Duración: {}\n'.format(elapsed)
        ret += u'Procesados: {} productos'.format(self.prod_processed)
        return ret

    @property
    def email_from(self):
        return self.env['ir.config_parameter'].get_param('email_from', '')

    @property
    def email_to(self):
        return self.env['ir.config_parameter'].get_param('email_notification',
                                                         '')

    @property
    def data_path(self):
        return self.env['ir.config_parameter'].get_param('data_path', '')

    @property
    def last_replication(self):
        """ Si import_only_new devolver ulima replicacion en el 2000
            Si no, devolver la fecha de la ultima replicacion
        """
        parameter_obj = self.env['ir.config_parameter']
        if not parameter_obj.get_param('import_only_new'):
            return '2000-01-01'
        else:
            return parameter_obj.get_param('last_replication')

    @last_replication.setter
    def last_replication(self, value):
        parameter_obj = self.env['ir.config_parameter']
        parameter_obj.set_param('last_replication', str(value))

    @api.model
    def process_invoice_discounts(self):
        invoices = self.env['account.invoice'].search(
            [('discount_processed', '=', False),
             ('partner_id.ref', '=', 'BULONFER'),
             ('state', 'in', ['open', 'paid']),
             ('type', '=', 'in_invoice')])

        for invoice in invoices:
            _logger.info('processing discounts on invoice '
                         '{}'.format(invoice.document_number))
            invoice.compute_invoice_discount()
