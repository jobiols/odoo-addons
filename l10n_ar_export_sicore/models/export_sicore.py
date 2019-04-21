# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from datetime import date, timedelta, datetime
import base64
import calendar

# Diseno de registro de exportacion segun documento de sicore
# https://www.afip.gob.ar/iva/documentos/IVAEspecificacion.pdf

WITHHOLDING = '6'
PERCEPTION = '7'


class AccountExportSicore(models.Model):
    _name = 'account.export.sicore'
    _description = 'account.export.sicore'

    year = fields.Integer(
        default=lambda self: self._default_year(),
        help='año del periodo',
        string='Año'
    )
    month = fields.Integer(
        default=lambda self: self._default_month(),
        help='mes del periodo',
        string='Mes'
    )
    period = fields.Char(
        compute="_compute_period",
        string='Periodo'
    )
    quincena = fields.Selection(
        [('0', 'Mensual'),
         ('1', 'Primera'),
         ('2', 'Segunda')],
        default=0
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
        'Desde',
        readonly=True,
        compute="_compute_dates"
    )
    date_to = fields.Date(
        'Hasta',
        readonly=True,
        compute="_compute_dates"
    )
    export_sicore_data = fields.Text(
        'Contenido archivo'
    )
    export_sicore_file = fields.Binary(
        'Descargar Archivo',
        compute="_compute_files",
        readonly=True
    )
    export_sicore_filename = fields.Char(
        'Archivo sicore',
        compute="_compute_files",
        readonly=True
    )

    @staticmethod
    def _last_month():
        today = date.today()
        first = today.replace(day=1)
        return first - timedelta(days=1)

    def _default_year(self):
        return self._last_month().year

    def _default_month(self):
        return self._last_month().month

    @api.onchange('year', 'month')
    @api.multi
    def _compute_period(self):
        for reg in self:
            reg.period = '{}/{}'.format(reg.year, reg.month)

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
    @api.depends('export_sicore_data')
    def _compute_files(self):
        for rec in self:
            # segun vimos aca la afip espera "ISO-8859-1" en vez de utf-8
            # filename sicore-30708346655-201901.txt

            cuit = rec.env.user.company_id.main_id_number
            if rec.date_from and rec.date_to:
                date = rec.date_from[:4] + rec.date_from[5:7]
            else:
                date = '000000'

            filename = 'sicore-%s-%s.txt' % (cuit, date)
            rec.export_sicore_filename = filename
            if rec.export_sicore_data:
                rec.export_sicore_file = base64.encodebytes(
                    rec.export_sicore_data.encode('ISO-8859-1'))

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

    def get_perception_invoices(self):
        """ Obtiene las facturas de cliente que tienen percepciones y que
            estan en el periodo seleccionado.
        """

        # busco el id de la etiqueta que marca los impuestos de Ganancias
        name = 'Ret/Perc SICORE Aplicada'
        account_tag_obj = self.env['account.account.tag']
        percSICORE = account_tag_obj.search([('name', '=', name)]).id

        invoice_obj = self.env['account.invoice']
        invoices = invoice_obj.search([
            ('date_invoice', '>=', self.date_from),
            ('date_invoice', '<=', self.date_to),
            ('state', 'in', ['open', 'paid']),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ])
        ret = invoice_obj

        for inv in invoices:
            if any([tax for tax in inv.tax_line_ids
                    if percSICORE in tax.tax_id.tag_ids.ids]):
                ret += inv
        return ret

    @api.multi
    def compute_sicore_data(self):

        line = ''
        for rec in self:
            if rec.doc_type == WITHHOLDING:

                # Retenciones
                payments = self.get_withholding_payments()
                data = []
                for payment in payments:

                    # Campo 01 -- Regimen
                    regimen = '1'
                    line = regimen.zfill(3)

                    # Campo 02 -- Cuit Agente
                    cuit = payment.payment_group_id.partner_id.main_id_number
                    line += cuit

                    # Campo 03 -- Fecha Retencion
                    date = datetime.strptime(payment.payment_date, '%Y-%m-%d')
                    date = date.strftime('%d/%m/%Y')
                    line += date

                    # Campo 04 -- Numero comprobante
                    line += payment.withholding_number[0:16].zfill(16)

                    # Campo 05 -- Importe retencion
                    amount = '{:.2f}'.format(payment.amount)
                    line += amount.zfill(16)

                    data.append(line)
            else:
                #  Percepciones
                # traer todas las facturas con percepciones en el periodo
                invoices = rec.get_perception_invoices()
                data = []
                for invoice in invoices:

                    # puede haber varios impuestos de percepcion en la factura
                    perception_taxes = invoice.tax_line_ids.filtered(
                        lambda r: r.tax_id.tax_group_id.type == 'perception')

                    for tax in perception_taxes:
                        # Campo 1 -- Regimen
                        regimen = '1'
                        line = regimen.zfill(3)

                        # Campo 2 Cuit Agente
                        cuit = invoice.partner_id.main_id_number
                        line = cuit

                        # Campo 3 -- Fecha de la percepcion
                        date = datetime.strptime(invoice.date_invoice,
                                                 '%Y-%m-%d')
                        date = date.strftime('%d/%m/%Y')
                        line += date

                        # Campo 4 -- Numero comprobante
                        line += invoice.document_number[0:16].zfill(16)

                        # Campo 5 -- Importe de percepcion
                        # ver si es invoice o refund
                        invoice = invoice.type == 'in_invoice'
                        amount = tax.amount if invoice else -tax.amount
                        line += '{:.2f}'.format(amount).zfill(11)

                data.append(line)

            rec.export_sicore_data = '\n'.join(data)
