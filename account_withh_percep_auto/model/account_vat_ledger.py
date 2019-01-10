# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
import base64
from datetime import datetime


class AccountVaLedger(models.Model):
    _inherit = 'account.vat.ledger'

    perceptions_file = fields.Binary(
        compute='_compute_perception_files',
        readonly=True
    )
    perceptions_filename = fields.Char(
        compute='_compute_perception_files',
        readonly=True,
    )
    REGINFO_PERCEPTIONS = fields.Text(
        readonly=True,
    )
    withholdings_file = fields.Binary(
        compute='_compute_withholding_files',
        readonly=True
    )
    withholdings_filename = fields.Char(
        compute='_compute_withholding_files',
        readonly=True,
    )
    REGINFO_WITHHOLDINGS = fields.Text(
        readonly=True,
    )

    @api.multi
    def compute_withholding_data(self):
        """ Llamado desde Form de IVA Compras, calcula las retenciones del
            periodo
        """
        res = []
        for pay in self.get_withholding_payments():

            # Campo 01 -- Cuit contribuyente retenido
            number = pay.partner_id.main_id_number
            cuit = '%s-%s-%s' % (number[0:2], number[2:10], number[10:])
            row = [cuit]

            # Campo 02 -- Fecha Retencion
            date = datetime.strptime(pay.payment_date, '%Y-%m-%d')
            date = date.strftime('%d/%m/%Y')
            row += [date]

            # Campo 03 -- Numero Sucursal
            # row += [tax.sequence[:4]]
            row += [pay.withholding_number[:4]]

            # Campo 04 -- Numero Emision
            # row += [tax.sequence[4:]]
            row += [pay.withholding_number[5:]]

            # Campo 05 -- Importe Retencion
            withholding = '{:011.2f}'.format(pay.computed_withholding_amount)
            row += [withholding]

            # Campo 06 -- Tipo Operacion
            row += ['A']

            res.append(''.join(row))

        self.REGINFO_WITHHOLDINGS = '\r\n'.join(res)

    @api.multi
    def compute_perception_data(self):
        """ Llamado desde Form de IVA Ventas, calcula las percepciones del
            periodo
        """
        res = []
        for inv in self.get_perception_invoices():

            # Campo 01 -- Cuit contribuyente percibido
            number = inv.partner_id.main_id_number
            cuit = '%s-%s-%s' % (number[0:2], number[2:10], number[10:])
            row = [cuit]

            # Campo 02 -- Fecha Percepcion
            date = datetime.strptime(inv.date_invoice, '%Y-%m-%d')
            date = date.strftime('%d/%m/%Y')
            row += [date]

            # Campo 03 -- Tipo de comprobante
            document_type = inv.journal_document_type_id.document_type_id
            if document_type.internal_type == 'invoice':
                type = 'F'
            if document_type.internal_type == 'credit_note':
                type = 'C'
            if document_type.internal_type == 'debit_note':
                type = 'D'
            row += [type]

            # Campo 04 -- Letra comprobante
            row += [document_type.document_letter_id.name]

            # Campo 05 -- Numero Sucursal
            # row += [tax.sequence[:4]]
            row += [inv.document_number[:4]]

            # Campo 06 -- Numero Emision
            # row += [tax.sequence[4:]]
            row += [inv.document_number[5:]]

            # Campo 07 -- Monto imponible
            # TODO Esto habria que sacarlo del tax
            tax = inv.tax_line_ids.filtered(
                lambda r: r.tax_id.tax_group_id.type == 'perception')
            amount = '{:012.2f}'.format(inv.amount_untaxed)
            row += [amount]

            # Campo 08 -- Importe de la percepcion
            perception = '{:011.2f}'.format(tax.amount)
            row += [perception]

            # Campo 09 -- Tipo Operacion
            row += ['A']

            res.append(''.join(row))

        self.REGINFO_PERCEPTIONS = '\r\n'.join(res)

    def get_perception_invoices(self):
        return self.env['account.invoice'].search([
            ('export_perception', '=', True),
            ('id', 'in', self.invoice_ids.ids)])

    def get_withholding_payments(self):
        return self.env['account.payment'].search([
            ('export_withholding', '=', True),
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to),
            ('state', '=', 'posted')])

    @api.depends('date_from', 'date_to', 'REGINFO_PERCEPTIONS')
    def _compute_perception_files(self):
        period = '%s_%s' % (self.date_from, self.date_to)
        self.perceptions_filename = '{}-perception.txt'.format(period)
        if self.REGINFO_PERCEPTIONS:
            self.perceptions_file = base64.encodestring(
                self.REGINFO_PERCEPTIONS.encode('ISO-8859-1'))

    @api.depends('date_from', 'date_to', 'REGINFO_WITHHOLDINGS')
    def _compute_withholding_files(self):
        period = '%s_%s' % (self.date_from, self.date_to)
        self.withholdings_filename = '{}-withholding.txt'.format(period)
        if self.REGINFO_WITHHOLDINGS:
            self.withholdings_file = base64.encodestring(
                self.REGINFO_WITHHOLDINGS.encode('ISO-8859-1'))
