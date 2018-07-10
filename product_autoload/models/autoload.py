# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import time
from datetime import datetime
import csv
from mappers import MAP_WRITE_DATE
from openerp import api, models, fields, registry
from mappers import ProductMapper


class ExceptionBarcodeDuplicated(Exception):
    def __init__(self, msg):
        self.message = msg


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
    created = fields.Integer(
        string="Created products"
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
                try:
                    item_obj.create(values)
                except:
                    raise ExceptionBarcodeDuplicated(
                        'Barcode Duplicated %s for product %s' %
                        (line[PC_BARCODE].strip(),
                         line[PC_PRODUCT_CODE].strip())
                    )

    def load_product(self, data_path):
        """ Carga todos los productos teniendo en cuenta la fecha
        """
        bulonfer_id = self.env['res.partner'].search(
            [('ref', '=', 'BULONFER')])
        if not bulonfer_id:
            raise Exception('Vendor Bulonfer not found')

        last_replication = self.last_replication
        _logger.info('REPLICATION: Load products '
                     'with timestamp > {}'.format(last_replication))

        prod_processed = prod_created = barc_changed = barc_created = 0
        with open(data_path + DATA, 'r') as file_csv:
            reader = csv.reader(file_csv)
            for line in reader:
                if line and line[MAP_WRITE_DATE] > last_replication:
                    obj = ProductMapper(line, data_path, bulonfer_id.ref)
                    stats = obj.execute(self.env)

                    if 'barc_created' in stats:
                        barc_created += 1
                    if 'barc_changed' in stats:
                        barc_changed += 1
                    if 'prod_processed' in stats:
                        prod_processed += 1
                    if 'prod_created' in stats:
                        prod_created += 1

            return {'barc_created': barc_created,
                    'barc_changed': barc_changed,
                    'prod_processed': prod_processed,
                    'prod_created': prod_created}

    @api.model
    def run(self, item=ITEM, productcode=PRODUCTCODE):
        """ Actualiza todos los productos.
        """
        config_obj = self.env['ir.config_parameter']
        email_from = config_obj.get_param('email_from', '')
        email_to = config_obj.get_param('email_notification', '')

        # empezamos a contar el tiempo de proceso
        start_time = time.time()
        data_path = self.data_path
        rec = self.create({})
        _logger.info('REPLICATION: Start #{}'.format(rec.id))
        try:
            start = time.strftime('%Y-%m-%d %H:%M:%S',
                                  time.localtime(start_time))
            rec.start_time = start

            # Cargar en memoria las tablas chicas
            self._section = self.load_section(data_path)
            self._family = self.load_family(data_path)

            _logger.info('REPLICATION: Load disk tables')
            # Cargar en bd las demas tablas
            self.load_item(data_path, item)
            self.load_productcode(data_path, productcode)

            # Aca carga solo los productos que tienen fecha de modificacion
            # posterior a la fecha de proceso y los actualiza o los crea segun
            # sea necesario
            stats = self.load_product(data_path)

            # terminamos de contar el tiempo de proceso
            elapsed_time = time.time() - start_time
            elapsed = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            self.send_email('Replicacion Bulonfer #{}'.format(rec.id),
                            self.get_stats(start, elapsed, stats),
                            email_from, email_to)

            self.last_replication = str(datetime.now())
            _logger.info('REPLICATION: End')

            rec.write({
                'name': '#{} Replicacion'.format(rec.id),
                'start_time': start,
                'elapsed_time': elapsed,
                'statistics': self.get_stats(start, elapsed, stats),
                'processed': stats['prod_processed'],
                'created': stats['prod_created']
            })

        except Exception as ex:
            _logger.error('Replicacion Bulonfer {}'.format(ex.message))
            with api.Environment.manage():
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    # Create a new environment with new cursor database
                    new_env = api.Environment(new_cr, self.env.uid,
                                              self.env.context)
                    # with_env replace original env for this method

                    self.with_env(new_env).create({
                        'name': '#{} ERROR'.format(rec.id),
                        'statistics': ex.message,
                    })  # isolated transaction to commit

                    self.with_env(new_env).send_email(
                        'Replicacion Bulonfer #{}, '
                        'ERROR'.format(rec.id), ex.message,
                        email_from, email_to)

                    new_env.cr.commit()  # Don't show invalid-commit
                    # don't need close cr because is closed when finish "with"
                    # don't need clear caches, is cleared when finish "with"

    @api.model
    def update_categories(self):
        config_obj = self.env['ir.config_parameter']
        email_from = config_obj.get_param('email_from', '')
        email_to = config_obj.get_param('email_notification', '')

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
                                email_from, email_to)
                raise Exception(text)

            # calcular el precio de lista
            prod.recalculate_list_price(item.margin)

            # buscar seccion o crearla en categorias
            sec_id = categ_obj.search([('name', '=', item.section),
                                       ('parent_id', '=', False)])
            if not sec_id:
                sec_id = categ_obj.create({'name': item.section,
                                           'property_cost_method': 'real',
                                           'removal_strategy_id': 1,
                                           'property_valuation': 'real_time'})

            # buscar seccion / familia o crearla
            sec_fam_id = categ_obj.search([('name', '=', item.family),
                                           ('parent_id.name', '=',
                                            item.section)])
            if not sec_fam_id:
                sec_fam_id = categ_obj.create({'name': item.family,
                                               'parent_id': sec_id.id,
                                               'property_cost_method': 'real',
                                               'removal_strategy_id': 1,
                                               'property_valuation':
                                                   'real_time'})

            # buscar seccion / familia / item o crearla
            categ_id = categ_obj.search([('name', '=', item.name),
                                         ('parent_id.name', '=', item.family),
                                         ('parent_id.parent_id.name', '=',
                                          item.section)])
            if not categ_id:
                categ_id = categ_obj.create({'name': item.name,
                                             'parent_id': sec_fam_id.id,
                                             'property_cost_method': 'real',
                                             'removal_strategy_id': 1,
                                             'property_valuation':
                                                 'real_time'})

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

    def get_stats(self, start, elapsed, stats):
        ret = u'Productos procesados: {}\n'.format(stats['prod_processed'])
        ret += u'Productos creados: {}\n'.format(stats['prod_created'])
        ret += u'Inicio: {}\n'.format(start)
        ret += u'Duración: {}\n'.format(elapsed)
        ret += u'Codigos de barra creados {}\n'.format(stats['barc_created'])
        ret += u'Codigos de barra modificados {}\n'.format(
            stats['barc_changed'])
        return ret

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

    @api.model
    def check_cost(self):
        """ Revisa los costos del cost history
        """
        import wdb; wdb.set_trace()
        stock_quant_obj = self.env['stock.quant']
        for sq in stock_quant_obj.search([]):
            print sq.cost,
            print sq.product_tmpl_id.standard_price

    @api.model
    def fix_category(self):
        """ corrige las categorias
        """
        for categ in self.env['product.category'].search([]):
            categ.property_cost_method = 'real'
            categ.property_valuation = 'real_time'
            categ.removal_strategy_id = 1
