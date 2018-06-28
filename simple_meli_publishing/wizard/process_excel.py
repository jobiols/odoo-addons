# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields
from openerp.exceptions import UserError, Warning
import base64
import tempfile
import openpyxl


class UploadPrices(models.TransientModel):
    _name = "simple_meli_publishing.process_excel"

    data = fields.Binary(
        required=True,
        string="Worksheet to process"
    )
    pdata = fields.Binary(
        required=False,
        string="Worksheet processed",
    )
    name = fields.Char(
        'File Name',
    )
    state = fields.Selection(
        [('load', 'Load'),  # load spreadsheet
         ('download', 'Download'),  # download spreadsheet
         ('error', 'Error')],  # show errors
        default="load"
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
                    u'ERROR in line {}, product "{}" not found'
                    u''.format(row['row'], row['default_code']))
            try:
                # check list price is a number
                float(row['list_price'])
            except ValueError as ve:
                raise UserError(
                    u'Error in line {}, list price "{}" not a number'
                    u''.format(row['row'], row['list_price']))

            try:
                # check standard price is a number
                float(row['standard_price'])
            except ValueError as ve:
                raise UserError(
                    u'Error in line {}, standard price "{}" not a number'
                    u''.format(row['row'], row['standard_price']))

    def process_data(self, data):
        product_obj = self.env['product.product']
        for row in data:
            domain = [('default_code', '=', row['default_code'])]
            prod = product_obj.search(domain)
            prod.list_price = float(row['list_price'])
            prod.standard_price = float(row['standard_price'])

    @api.multi
    def load_file(self):
        for pp in self:
            #import wdb;wdb.set_trace()
            pp.state = 'download'
            pp.pdata = pp.data


        """
        data = base64.decodestring(self.data)
        (fileno, fp_name) = tempfile.mkstemp('.xlsx', 'openerp_')
        openfile = open(fp_name, "w")
        openfile.write(data)
        openfile.close()
        return



        wb = openpyxl.load_workbook(filename=fp_name, read_only=True,
                                    data_only=True)
        data = self.read_data(wb.active)
        self.check_data(data)
        self.process_data(data)
        """