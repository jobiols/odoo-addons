# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields, _
import base64
import tempfile
import logging

_logger = logging.getLogger(__name__)

try:
    import openpyxl
except (ImportError, IOError) as err:
    _logger.debug(err)

# info de como es la tabla, es una lista de tuplas y cada tupla tiene
# Nombre del campo, Requerido para Crear, Requerido para Actualizar y tipo
INFO = [
    {'name': 'default_code', 'create_req': True, 'update_req': True,
     'type': 'str'},
    {'name': 'currency', 'create_req': True, 'update_req': True,
     'type': 'currency'},
    {'name': 'cost', 'create_req': True, 'update_req': True, 'type': 'number'},
    {'name': 'price', 'create_req': True, 'update_req': True,
     'type': 'number'},
    {'name': 'name', 'create_req': True, 'update_req': False, 'type': 'str'},
    {'name': 'purchase_tax', 'create_req': True, 'update_req': False,
     'type': 'tax'},
    {'name': 'sale_tax', 'create_req': True, 'update_req': False,
     'type': 'tax'},
    {'name': 'barcode', 'create_req': False, 'update_req': False,
     'type': 'str'},
    {'name': 'meli', 'create_req': False, 'update_req': False, 'type': 'str'},
    {'name': 'parent', 'create_req': False, 'update_req': False,
     'type': 'default_code'}
]


class ImportWorksheet(models.TransientModel):
    _name = "product_upload.import_worksheet"

    data = fields.Binary(
            'File',
            required=True
    )
    name = fields.Char(
            'Filename',
            readonly=True
    )

    def read_data(self, sheet):
        """ Read the spreadsheet into a data structure
        """
        def check(info, col, create):
            """ chequear los datos y generar errores si estan mal
            """
            if col > sheet.max_column:
                self.add_error(_('out of bound col variable'))

            err = _('in row %d field %s of sheet %s')

            value = row[col].value

            data_type = info['type']
            name = info['name']
            req = info['create_req'] if create else info['update_req']

            if data_type == 'currency':
                if not (value == 'USD' or value == 'ARS'):
                    text = _('Invalid Currency must be ARS or USD') + \
                           ' ' + err % (row[col].row, name, sheet.title)
                    self.add_error(text)
                return {name: value}

            if data_type == 'str':
                if not (isinstance(value, (str, unicode)) or
                        (value is None and not req)):

                    text = _('Cell must contain text') + \
                           ' ' + err % (row[col].row, name, sheet.title)
                    self.add_error(text)
                if value:
                    value = value.strip()
                return {name: value}

            if data_type == 'number':
                if not (isinstance(value, (float, int, long)) or
                        (value is None) and not req):
                    row_ = row[col].row if row[col].value is not None else 0
                    text = _('Cell must contain a number') + \
                           ' ' + err % (row_, name, sheet.title)
                    self.add_error(text)
                return {name: value}

            if data_type == 'default_code':
                if not (isinstance(value, (str, unicode)) or
                        (value is None) and not req):
                    text = _('Cell must contain text') + \
                           ' ' + err % (row[col].row, name, sheet.title)
                    self.add_error(text)

                product_obj = self.env['product.template']
                product = product_obj.search([('default_code', '=', value)])
                if not product:
                    text = _('Product %s from parent col not found') + \
                           ' ' + err % (
                        product.default_code, row[col].row, sheet.title)
                    self.add_error(text)
                    if value:
                        value = value.strip()
                return {name: value}

            if data_type == 'tax':
                if not (isinstance(value, (float)) or (value is None) and not req) or (value >= 1):
                    row_ = row[col].row if row[col].value is not None else 0
                    text = _('The Cell must contain IVA, a float number less than 1') + \
                           ' ' + err % (row_, name, sheet.title)
                    self.add_error(text)
                return {name: value}


            self.add_error(_('internal error !!'))

        if sheet.max_column < 10:
            self.add_error(_('Checkout the header in the sheet %s it seems some columns are missing.') % sheet.title)
            return

        ret = []
        for row in sheet.iter_rows(min_row=2, min_col=1,
                                   max_row=sheet.max_row,
                                   max_col=sheet.max_column):
            line = {}

            if row[0].value is not None:
                # si hay que crear el producto devuelve True
                create = self.check_create(row[0].value)
                for idx, info in enumerate(INFO):
                    value = check(info, idx, create)
                    line.update(value)

                # si no hay errores agrego la linea
                if not self.log.errors:
                    ret.append(line)

        return ret

    def check_create(self, default_code):
        prod_obj = self.env['product.template']
        prod = prod_obj.search([('default_code', '=', default_code.strip())])
        return True if prod else False

    def process_data(self, data, vendor):
        """ Process data structure creating / updating products
        """

        def choose_tax(tax_sale):
            for tax in tax_sale:
                if tax.amount != 0:
                    # si no es cero es ese
                    return tax.id
                else:
                    # si es iva cero busco que sea exento
                    if tax.tax_group_id.afip_code == 2:
                        return tax.id

        product_obj = self.env['product.template']
        currency_obj = self.env['res.currency']
        barcode_obj = self.env['product.barcode']
        tax_obj = self.env['account.tax']

        for row in data:
            domain = [('default_code', '=', row['default_code'])]
            prod = product_obj.search(domain)
            data = {}

            if self.env.user.currency_id.name != row['currency']:
                pc = currency_obj.search([('name', '=', row['currency'])])
                data['force_currency_id'] = pc.id
            if row['name']:
                data['name'] = row['name']
            if row['meli']:
                data['meli_code'] = row['meli']
            if row['parent']:
                data['parent_price_product'] = row['parent']

            data['type'] = 'product'
            data['invoice_policy'] = 'order'
            data['purchase_method'] = 'purchase'
            data['sale_delay'] = 0

            if not prod:
                data['default_code'] = row['default_code']
                prod = product_obj.create(data)
                self.add_create()
                _logger.info('create product %s' % prod.default_code)
            else:
                prod.ensure_one()
                prod.write(data)
                self.add_update()
                _logger.info('update product %s' % prod.default_code)

            if row['barcode']:
                barcode_obj.add_barcode(prod, row['barcode'])

            if row['purchase_tax']:
                # actualiza iva compras
                tax_purchase_id = tax_obj.search(
                        [('amount', '=', row['purchase_tax'] * 100),
                         ('tax_group_id.tax', '=', 'vat'),
                         ('type_tax_use', '=', 'purchase')])
                # analizando el iva
                tax = choose_tax(tax_purchase_id)

                # esto reemplaza todos los registros por el tax que es un id
                prod.supplier_taxes_id = [(6, 0, [tax])]

            if row['sale_tax']:
                # actualiza IVA ventas
                tax_sale_id = tax_obj.search(
                        [('amount', '=', row['sale_tax'] * 100),
                         ('tax_group_id.tax', '=', 'vat'),
                         ('type_tax_use', '=', 'sale')])
                # analizando el iva
                tax = choose_tax(tax_sale_id)

                # esto reemplaza todos los registros por el tax que es un id
                prod.taxes_id = [(6, 0, [tax])]

            prod.set_prices(row['cost'], vendor, price=row['price'],
                            manual=True)
            prod.set_invoice_cost()

    @api.multi
    def import_file(self):
        """ Se ejecuta desde el boton import file del wizard, sube la planilla
            y la deja en un archivo temporario
        """
        for rec in self:
            # obtener el record log
            log_obj = self.env['product_upload.log']
            current_id = self.env.context.get('default_active_id', False)
            self.log = log_obj.search([('id', '=', current_id)])
            if not self.log:
                # TODO esto no anda, ver porque
                raise Exception('unknown error')

            data = base64.decodestring(rec.data)
            (fileno, fp_name) = tempfile.mkstemp('.xlsx', 'openerp_')

            # escribir la planilla en un temporario
            with open(fp_name, 'w') as ws:
                ws.write(data)

            self.process_tmp_file(fp_name)

    def process_tmp_file(self, tmp_file):
        """ Procesa la planilla que esta en el archivo temporario
        """

        # leer la planilla del temporario en solo lectura
        wb = openpyxl.load_workbook(filename=tmp_file, read_only=True,
                                    data_only=True)

        # cada hoja de la planilla es un vendor
        partner_obj = self.env['res.partner']
        vendors = wb.sheetnames
        for vendor in vendors:
            partner = partner_obj.search([('ref', '=', vendor)])
            if not partner:
                self.add_error(_('Vendor ref %s not found.') % vendor)
                break

            self.add_vendor(vendor)
            data = self.read_data(wb[vendor])

            if self.log.errors:
                break

            if data:
                self.process_data(data, vendor)
                self.log.state = 'done'

    def add_error(self, text):
        """ add an error to log
        """
        self.log.state = 'error'
        self.log.errors += 1
        self.log.error_ids.create({
            'name': text,
            'log_id': self.log.id
        })

    def add_create(self):
        """ Increment Created
        """
        self.log.created_products += 1

    def add_update(self):
        """ Increment Created
        """
        self.log.updated_products += 1

    def add_vendor(self, vendor):
        """ Add a vendor to a list
        """
        if not self.log.vendors:
            self.log.vendors = vendor
        else:
            self.log.vendors += ', ' + vendor
