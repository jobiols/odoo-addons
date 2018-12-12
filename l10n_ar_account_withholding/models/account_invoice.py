# -*- coding: utf-8 -*-
from openerp import models, api, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_date_assign(self):
        """ sobreescribe el primer metodo del workflow invoice_open """
        self.compute_perceptions()
        return super(AccountInvoice, self).action_date_assign()

    def compute_perceptions(self):
        """ agrega el impuesto de percepcion si la alicuota != 0 """
        invoice_id = self.ensure_one()

        # si la fecha es false poner la fecha de hoy
        if invoice_id.date_invoice:
            date_invoice = invoice_id.date_invoice
        else:
            date_invoice = fields.Date.context_today(self)
        ctx = {
            'date_invoice': date_invoice,
            'invoice_company': invoice_id.company_id
        }

        # obtener la alicuota para este partner, buscarla en base de datos o
        # si no la tengo consultar el ws de ARBA
        _ = invoice_id.partner_id.with_context(ctx)
        perception = _.get_arba_alicuota_percepcion()

        # si la alicuota es cero termina sin hacer nada
        if not perception:
            return

        tax_obj = self.env['account.tax']

        # obtener los impuestos de percepcion FUERZO SOLO EL DE IIBB
        tax_ids = tax_obj.search([('type_tax_use', '=', 'sale'),
                                 ('tax_group_id.type', '=', 'perception'),
                                  ('name', 'like', '%IIBB%')])

        base = invoice_id.amount_untaxed

        for tax_id in tax_ids:
            res = tax_id.with_context(ctx).compute_all(base)
            tax = res['taxes'][0]
            val = {
                'base': base,
                'invoice_id': invoice_id.id,
                'name': tax_id.name,
                'tax_id': tax_id.id,
                'amount': base * perception,
                'manual': True,
                'sequence': 99,
                'account_analytic_id': False,
                'account_id': invoice_id.type in ('out_invoice', 'in_invoice') and (
                    tax['account_id'] or False) or (
                    tax['refund_account_id'] or False),
            }

            self.env['account.invoice.tax'].create(val)

    @api.multi
    def _get_tax_factor(self):
        tax_factor = super(AccountInvoice, self)._get_tax_factor()
        doc_letter = self.document_type_id.document_letter_id.name
        # if we receive B invoices, then we take out 21 of vat
        # this use of case if when company is except on vat for eg.
        if tax_factor == 1.0 and doc_letter == 'B':
            tax_factor = 1.0 / 1.21
        return tax_factor

    @api.multi
    def get_taxes_values(self):
        """
        Hacemos esto para disponer de fecha de factura y cia para calcular
        impuesto con código python (por ej. para ARBA).
        Aparentemente no se puede cambiar el contexto a cosas que se llaman
        desde un onchange (ver https://github.com/odoo/odoo/issues/7472)
        entonces usamos este artilugio
        """
        date_invoice = self.date_invoice or fields.Date.context_today(self)
        self.env.context.date_invoice = date_invoice
        self.env.context.invoice_company = self.company_id
        return super(AccountInvoice, self).get_taxes_values()


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.one
    def _compute_price(self):
        # ver nota en get_taxes_values
        invoice = self.invoice_id
        date_invoice = invoice.date_invoice or fields.Date.context_today(self)
        self.env.context.date_invoice = date_invoice
        self.env.context.invoice_company = self.company_id
        return super(AccountInvoiceLine, self)._compute_price()
