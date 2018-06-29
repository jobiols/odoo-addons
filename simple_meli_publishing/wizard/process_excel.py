# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, models, fields
from openerp.exceptions import UserError, Warning
import base64
import tempfile
import openpyxl


class SimpleMeliPublishing(models.TransientModel):
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

    def process_data(self, fp_name):
        product_obj = self.env['product.product']

        # open worksheet
        wb = openpyxl.load_workbook(filename=fp_name,
                                    read_only=False,
                                    data_only=True)
        wb.active


    @api.multi
    def load_file(self):
        for rec in self:
            #import wdb;wdb.set_trace()

            # escribir la data en un archivo temporario
            data = base64.decodestring(rec.data)
            (fileno, fp_name) = tempfile.mkstemp('.xlsx', 'openerp_')
#            openfile = open(fp_name, "w")
#            openfile.write(data)
#            openfile.close()
            with open(fp_name, "w") as worksheet:
                worksheet.write(data)

            # procesar el archivo
            #self.process_data(fp_name)

            # leer el archivo temporario para hacer download
            with open(fp_name, "r") as worksheet:
                rec.pdata = base64.encodestring(worksheet.read())

            # cambiar la vista para que descarguen el archivo
            rec.state = 'download'
