# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
from dateutil import relativedelta
import base64
from datetime import datetime
import calendar

# Diseno de registro de exportacion segun documento de ARBA
# https://www.arba.gov.ar/Archivos/Publicaciones/dise%C3%B1o_de_registros_bancos.pdf
# 1.1. Percepciones ( excepto actividad 29, 7 quincenal y 17 de Bancos)
# 1.7. Retenciones ( excepto actividad 26, 6 de Bancos y 17 de Bancos y No Bancos)

WITHHOLDING = '6'
PERCEPTION = '7'


class AccountExportArba(models.Model):
    _name = 'account.export.arba'
    _description = 'account.export.arba'

    year = fields.Integer(
        default=datetime.now().year,
        help='año del periodo',
        string='Año'
    )
    quincena = fields.Selection(
        [('0', 'Mensual'),
         ('1', 'Primera'),
         ('2', 'Segunda')],
        default=0
    )
    month = fields.Integer(
        default=datetime.now().month,
        help='mes del periodo',
        string='Mes'
    )
    doc_type = fields.Selection(
        [
            (WITHHOLDING, 'Retencion'),
            (PERCEPTION, 'Percepcion')
        ],
        string="Tipo de archivo",
        default="6"
    )
    date_from = fields.Date(
        'Fecha inicio',
        readonly=True,
        compute="_compute_dates"
    )
    date_to = fields.Date(
        'Fecha fin',
        readonly=True,
        compute="_compute_dates"
    )
    export_arba_data = fields.Text(
        'Contenido archivo'
    )
    export_arba_file = fields.Binary(
        'Descargar Archivo',
        compute="_compute_files",
        readonly=True
    )
    export_arba_filename = fields.Char(
        'Archivo ARBA',
        compute="_compute_files",
        readonly=True
    )

    @api.onchange('year', 'month', 'quincena', 'doc_type')
    @api.multi
    def _compute_dates(self):
        """ Dado el mes y el año calcular el primero y el ultimo dia del
            periodo
        """
        for rec in self:
            # Las retenciones se hacen por mes
            if rec.doc_type == WITHHOLDING:
                rec.quincena = 0

            dts = datetime(rec.year, rec.month, 1)
            last_day = calendar.monthrange(rec.year, rec.month)[1]
            dte = datetime(rec.year, rec.month, last_day)

            if rec.quincena == '1':
                dts = datetime(rec.year, rec.month, 1)
                dte = datetime(rec.year, rec.month, 15)
            if rec.quincena == '2':
                dts = datetime(rec.year, rec.month, 16)
                last_day = calendar.monthrange(rec.year, rec.month)[1]
                dte = datetime(rec.year, rec.month, last_day)

            rec.date_from = dts.strftime('%Y-%m-%d')
            rec.date_to = dte.strftime('%Y-%m-%d')

    @api.multi
    @api.depends('export_arba_data')
    def _compute_files(self):

        self.ensure_one()
        # segun vimos aca la afip espera "ISO-8859-1" en vez de utf-8
        # http://www.planillasutiles.com.ar/2015/08/
        # como-descargar-los-archivos-de.html
        # filename AR-30708346655-2019010-7-LOTE1.txt
        #             |  cuit   | |fech|x y
        # x quincena
        # y ret / perc
        # quincena = 1 primera, 2 segunda 0 mensual

        cuit = self.env.user.company_id.main_id_number
        if self.date_from and self.date_to:
            date = self.date_from[:4] + self.date_from[5:7]
        else:
            date = '000000'
        doc_type = WITHHOLDING
        quincena = self.quincena

        filename = 'AR-%s-%s%s-%s-LOTE1.txt' % (cuit, date, quincena, doc_type)
        self.export_arba_filename = filename
        if self.export_arba_data:
            self.export_arba_file = base64.encodestring(
                self.export_arba_data.encode('ISO-8859-1'))

    def get_withholding_payments(self):
        """ Obtiene los pagos a proveedor que son retenciones y que
            estan en el periodo seleccionado
        """
        return self.env['account.payment'].search([
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to),
            ('state', '=', 'posted'),
            ('journal_id.inbound_payment_method_ids.code', '=', 'withholding')]
        )

    @api.multi
    def compute_arba_data(self):

        for rec in self:
            if rec.doc_type == WITHHOLDING:

                # Retenciones
                payments = self.get_withholding_payments()
                data = []
                for payment in payments:

                    # Campo 01 -- Cuit contribuyente retenido
                    cuit = payment.payment_group_id.partner_id.main_id_number
                    cuit = '%s-%s-%s' % (cuit[0:2], cuit[2:10], cuit[10:])
                    line = cuit

                    # Campo 02 -- Fecha de la retencion
                    date = datetime.strptime(payment.payment_date, '%Y-%m-%d')
                    date = date.strftime('%d/%m/%Y')
                    line += date

                    # Campo 03 -- Numero de sucursal
                    line += payment.withholding_number[:4]

                    # Campo 04 -- Numero de emision
                    line += payment.withholding_number[5:]

                    # Campo 05 -- Importe de Retencion
                    amount = '{:.2f}'.format(payment.amount)
                    line += amount

                    # Campo 06 -- Tipo de operacion
                    line += 'A'

                    data.append(line)
            else:
                #  Percepciones
                invoices = rec.get_perception_invoices()
                data = []
                for invoice in invoices:
                    # puede haber varios impuestos de percepcion en la factura
                    perception_taxes = invoice.tax_line_ids.filtered(
                        lambda r: r.tax_id.tax_group_id.type == 'perception')

                    for tax in perception_taxes:
                        # Campo 1 -- Cuit contribuyente percibido
                        cuit = invoice.partner_id.main_id_number
                        cuit = '%s-%s-%s' % (cuit[0:2], cuit[2:10], cuit[10:])
                        line = cuit

                        # Campo 2 -- Fecha de la percepcion
                        date = datetime.strptime(invoice.date_invoice,
                                                 '%Y-%m-%d')
                        date = date.strftime('%d/%m/%Y')
                        line += date

                        # Campo 3 -- Tipo de comprobante
                        line += invoice.display_name

                        # Campo 4 -- Letra comprobante
                        line += invoice.display_name

                        # Campo 5 -- Numero Surursal
                        line += invoice.display_name

                        # Campo 6 -- Numero Emision
                        line += invoice.display_name

                        # Campo 7 -- Monto imponible
                        if invoice.type == 'in_refund':
                            amount = tax.amount
                        line += invoice.total_unsigned

                        # Campo 6 -- Importe de percepcion
                        if invoice.type == 'in_refund':
                            amount = tax.amount * (-1)
                        else:
                            amount = tax.amount

                        line = '{:.2f}'.format(amount)

                data.append(line)

            rec.export_arba_data = '\n'.join(data)
