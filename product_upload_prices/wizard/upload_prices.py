# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields, _
from openerp.exceptions import UserError
import base64
import tempfile
import openpyxl


class UploadPrices(models.TransientModel):
    _name = "product_upload_prices.upload_prices"

    data = fields.Binary(
        'File',
        required=True
    )
    name = fields.Char(
        'Filename',
        readonly=True
    )

    @staticmethod
    def read_data(sheet):
        ret = []
        row_number = 0
        for row in sheet.iter_rows(min_row=1, min_col=1,
                                   max_col=3, max_row=40000):
            row_number += 1
            ret.append({
                'default_code': str(row[0].value),
                'list_price': row[1].value,
                'standard_price': row[2].value,
                'row': row_number
            })
        return ret

    def check_data(self, data):
        product_obj = self.env['product.product']
        for row in data:
            # check product exists
            domain = [('default_code', '=', row['default_code'])]
            if not product_obj.search(domain):
                raise UserError(
                    _(u'ERROR in line %s, product "%s" not found') %
                    (row['row'], row['default_code']))
            try:
                # check list price is a number
                float(row['list_price'])
            except (ValueError, TypeError):
                raise UserError(
                    _(u'Error in line %s, list price "%s" not a number') %
                    (row['row'], row['list_price']))
            try:
                # check standard price is a number
                float(row['standard_price'])
            except (ValueError, TypeError):
                raise UserError(
                    _(u'Error in line %s, standard price "%s" not a number') %
                    (row['row'], row['standard_price']))

    def process_data(self, data):
        product_obj = self.env['product.product']
        for row in data:
            domain = [('default_code', '=', row['default_code'])]
            prod = product_obj.search(domain)
            prod.list_price = float(row['list_price'])
            prod.standard_price = float(row['standard_price'])

    @api.multi
    def import_file(self):
        data = base64.decodestring(self.data)
        (fileno, fp_name) = tempfile.mkstemp('.xlsx', 'openerp_')
        openfile = open(fp_name, "w")
        openfile.write(data)
        openfile.close()
        wb = openpyxl.load_workbook(filename=fp_name, read_only=True,
                                    data_only=True)
        data = self.read_data(wb.active)
        self.check_data(data)
        self.process_data(data)