# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import base64
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class AccountVaLedger(models.Model):
    _inherit = 'account.vat.ledger'

    withholdings_s_file = fields.Binary(
        compute='_compute_s_withholding_files',
        readonly=True,
        string="Retenciones Sufridas"
    )
    withholdings_s_filename = fields.Char(
        compute='_compute_s_withholding_files',
        readonly=True,
    )
    REGINFO_S_WITHHOLDINGS = fields.Text(
        readonly=True,
        string="Datos de retenciones a descargar"
    )
    perceptions_s_file = fields.Binary(
        compute='_compute_s_perception_files',
        readonly=True,
        string="Percepciones sufridas"
    )
    perceptions_s_filename = fields.Char(
        compute='_compute_s_perception_files',
        readonly=True
    )
    REGINFO_S_PERCEPTIONS = fields.Text(
        readonly=True,
        string="Datos de percepciones a descargar"
    )

    @staticmethod
    def translate_tax(type):
        if type == 'vat':
            return 'IVA'
        if type == 'profits':
            return 'Ganancias'
        if type == 'gross_income':
            return 'IIBB'
        else:
            return 'Desconocido'

    @api.multi
    def compute_s_perception_data(self):
        """ Llamado desde Form de IVA Compras, calcula las percepciones
            sufridas en el periodo.
        """
        _logger.info('Computing suffered perception data')

        res = ['Cuit que percibe, Fecha percepcion, Factura, Monto percibido, '
               'Impuesto, Jurisdiccion']

        for invoice in self.get_perception_invoices():
            # puede haber varios impuestos de percepcion en la factura

            perception_taxes = invoice.tax_line_ids.filtered(
                lambda r: r.tax_id.tax_group_id.type == 'perception')
            for tax in perception_taxes:

                # Campo 01 -- Cuit contribuyente que genera la percepcion
                number = invoice.partner_id.main_id_number
                cuit = '%s-%s-%s' % (number[0:2], number[2:10], number[10:])
                row = [cuit]

                # Campo 02 -- Fecha Percepcion
                date = datetime.strptime(invoice.date_invoice, '%Y-%m-%d')
                date = date.strftime('%d/%m/%Y')
                row += [date]

                # Campo 03 -- nombre de la factura
                row += [invoice.display_name]

                # Campo 05 -- Importe percepcion
                if invoice.type == 'in_refund':
                    amount = tax.amount * (-1)
                else:
                    amount = tax.amount

                withholding = '{:.2f}'.format(amount)
                row += [withholding]

                # Campo 06 -- Impuesto
                tax_name = tax.tax_id.tax_group_id.tax
                row += [self.translate_tax(tax_name)]

                # Campo 07 Jurisdiccion
                tags = tax.tax_id.tag_ids
                if tax.tax_id.tax_group_id.tax == 'gross_income':
                    state = tags.filtered(lambda r: r.jurisdiction_code)
                    if state:
                        row += [state.name]
                    else:
                        row += ['Desconocido']
                if tax.tax_id.tax_group_id.tax in ['profits', 'vat']:
                    row += ['Nacional']

                res.append(', '.join(row))

        self.REGINFO_S_PERCEPTIONS = '\r\n'.join(res)

    @api.multi
    def compute_s_withholding_data(self):
        """ Llamado desde Form de IVA Ventas, calcula las retenciones
            sufridas en el periodo.
        """
        _logger.info('Computing suffered withholding data')
        res = ['Cuit que retiene, Fecha retencion, Nro retencion, Base, '
               'Monto retenido, Impuesto, Jurisdicc']
        for payment in self.get_withholding_payments():

            # Campo 01 -- Cuit que genera la retencion
            number = payment.payment_group_id.partner_id.main_id_number
            cuit = '%s-%s-%s' % (number[0:2], number[2:10], number[10:])
            row = [cuit]

            # Campo 02 -- Fecha de la retencion
            date = datetime.strptime(payment.payment_date, '%Y-%m-%d')
            date = date.strftime('%d/%m/%Y')
            row += [date]

            # Campo 05 -- Numero de Retencion
            row += [payment.withholding_number]

            # Campo 07 -- Base de la retencion
            base = '{:.2f}'.format(payment.withholding_base_amount)
            row += [base]

            # Campo 07 -- Monto de la retencion
            amount = '{:.2f}'.format(payment.amount)
            row += [amount]

            # Campo 08 -- Impuesto
            tax = payment.tax_withholding_id.tax_group_id.tax
            row += [self.translate_tax(tax)]

            # Campo 09 -- Jurisdiccion
            tags = payment.tax_withholding_id.tag_ids
            if tax == 'gross_income':
                state = tags.filtered(lambda r: r.jurisdiction_code)
                if state:
                    row += [state.name]
                else:
                    row += ['Desconocido']
            if tax in ['profits', 'vat']:
                row += ['Nacional']

            res.append(', '.join(row))

        self.REGINFO_S_WITHHOLDINGS = '\r\n'.join(res)

    def get_withholding_payments(self):
        """ Obtiene los pagos de cliente que tienen retenciones y que
            estan en el periodo seleccionado
        """
        return self.env['account.payment'].search([
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to),
            ('state', '=', 'posted'),
            ('journal_id.inbound_payment_method_ids.code', '=', 'withholding')]
        )

    def get_perception_invoices(self):
        """ Obtiene las facturas de proveedor que tienen percepciones y que
            estan en el diario seleccionado al crear el libro.
        """
        ret = self.env['account.invoice']
        for inv in self.invoice_ids:
            if any([tax for tax in inv.tax_line_ids
                    if tax.tax_id.tax_group_id.type == 'perception']):
                ret += inv
        return ret

    @api.depends('date_from', 'date_to', 'REGINFO_S_PERCEPTIONS')
    def _compute_s_perception_files(self):
        period = '%s_%s' % (self.date_from, self.date_to)
        self.perceptions_s_filename = '{}-perception.txt'.format(period)
        if self.REGINFO_S_PERCEPTIONS:
            self.perceptions_s_file = base64.encodestring(
                self.REGINFO_S_PERCEPTIONS.encode('ISO-8859-1'))

    @api.depends('date_from', 'date_to', 'REGINFO_S_WITHHOLDINGS')
    def _compute_s_withholding_files(self):
        period = '%s_%s' % (self.date_from, self.date_to)
        self.withholdings_s_filename = '{}-withholding.txt'.format(period)
        if self.REGINFO_S_WITHHOLDINGS:
            self.withholdings_s_file = base64.encodestring(
                self.REGINFO_S_WITHHOLDINGS.encode('ISO-8859-1'))
