# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
import base64
from datetime import datetime


class AccountVaLedger(models.Model):

    _inherit = "account.vat.ledger"

    sircar_file = fields.Binary(
        'Sircar File',
        compute='get_sircar_files',
        readonly=True
        )
    sircar_filename = fields.Char(
        'Sircar Filename',
        readonly=True,
        compute='get_sircar_files',
        )
    REGINFO_SIRCAR = fields.Text(
        'REGINFO_SIRCAR',
        readonly=True,
        )

    @api.one
    def compute_sircar_data(self):
        self.do_compute_sircar_data()

    @api.one
    @api.depends('period_id.name', 'REGINFO_SIRCAR')
    def get_sircar_files(self):
        fname = self.period_id.name.replace('/', '-') if self.period_id else 'unknown'
        self.sircar_filename = 'SIRCAR-{}.txt'.format(fname)
        if self.REGINFO_SIRCAR:
            self.sircar_file = base64.encodestring(
                    self.REGINFO_SIRCAR.encode('ISO-8859-1'))

    @api.one
    def do_compute_sircar_data(self):
        invoices = self.get_sircar_invoices()
        rec_no = 0
        res = []
        for inv in invoices:
            # Campo 01 -- Numero de registro
            rec_no += 1
            row = [str(rec_no)]

            # Campo 02 -- Tipo de comprobante
            row += ['1']

            # Campo 03 -- Letra del comprobante
            row += [inv.journal_document_class_id.afip_document_class_id.document_letter_id.name]

            # Campo 04 -- Número de Comprobante (incluye el punto de venta)
            row += [inv.afip_document_number.replace('-', '')]

            # Campo 05 -- CUIT Contribuyente involucrado en la transacción Comercial Numérico(11) 30100100106
            document_number = inv.partner_id.document_number if inv.partner_id.document_number else 'sin documento'
            row += [document_number]

            # Campo 06 -- Fecha de Percepción (en formato dd/mm/aaaa) dd/mm/aaaa 03/12/2001
            row += [datetime.strptime(inv.date_invoice, '%Y-%m-%d').strftime('%d/%m/%Y')]

            # Campo 07 -- Monto Sujeto a Percepción (numérico sin separador de miles) 999999999.99 12342.03
            untaxed = inv.amount_untaxed
            row += ['{:.2f}'.format(untaxed)]

            # Campo 08 -- Alícuota (porcentaje sin separador de miles) 999.99 42.03
            alic = 1.0
            row += ['{:.2f}'.format(alic)]

            # Campo 09 -- Monto Percibido (campo 7 por el campo 8 y dividirlo por 100)
            # hay que sumarle 0.0000000001 para que el redondeo de igual que el de la AFIP
            row += ['{:.2f}'.format(round(untaxed * alic / 100 + 0.0000000001, 2))]

            # Campo 10 -- Tipo de Régimen de Retención
            row += ['70']

            # Campo 11 -- Jurisdicción
            row += ['916']

            res.append(','.join(row))

        self.REGINFO_SIRCAR = '\r\n'.join(res)

    @api.multi
    def get_sircar_invoices(self):
        self.ensure_one()
        return self.env['account.invoice'].search([
            ('export_to_sircar', '=', True),
            ('id', 'in', self.invoice_ids.ids)])
