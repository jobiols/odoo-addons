# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from openerp import api, models
from datetime import datetime, timedelta

CUENTA_CORRIENTE = 'Cuenta Corriente'


class InvoiceReport(models.AbstractModel):
    _name = 'report.account_cash_report.invoice_report'

    def initial_balance(self, account_id, date_to):
        """ Devuelve el balance de la cuenta al dia anterior a la fecha
            dada, es lo que hay en la cuenta al iniciar el dia.
        """
        # obtener el dia anterior
        date = datetime.strptime(date_to, '%Y-%m-%d')
        date_to = datetime.strftime(date - timedelta(1), '%Y-%m-%d')

        trial_balance = self.env['report.account.report_trialbalance']
        account_res = trial_balance.with_context(date_to=date_to). \
            _get_accounts(account_id, 'movement')

        ret = 0
        for account in account_res:
            ret = account['balance']

        return ret

    @staticmethod
    def _get_journal_names(invoice):
        """ obtener una lista de medios de pago con los que se pago esta
            factura
        """
        payments = invoice.payments_widget.replace('false', 'False')
        payments = eval(payments)
        if payments:
            payments = payments['content']

            journals = []
            for payment in payments:
                if payment['journal_name'] not in journals:
                    journals.append(payment['journal_name'])

            if invoice.state == 'open':
                journals.append(CUENTA_CORRIENTE)

            return ', '.join(journals)

        return CUENTA_CORRIENTE

    def _get_invoices(self, data):
        """ Obtener todas las facturas validadas por la cajera de esta caja
            que son al cliente, y que estan en el periodo.
        """
        domain = [
            ('date', '>=', data['date_from']),
            ('date', '<=', data['date_to']),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ]

        invoice_obj = self.env['account.invoice']
        ret = []
        total = total_residual = 0
        for invoice in invoice_obj.search(domain):
            journal_names = self._get_journal_names(invoice)
            inv = {
                'number': invoice.display_name,
                'total': invoice.amount_total_signed,
                'journal': journal_names,
                'partner': invoice.partner_id.name,
                'salesperson': invoice.user_id.name
            }
            total += invoice.amount_total_signed
            total_residual += invoice.residual
            ret.append(inv)

        return ret, total, total_residual

    def _get_journals(self, data, journals, total_res):
        """ obtiene los medios de pago y el total acumulado en cada uno en el
            periodo considerado
        """

        ret = []
        total = 0
        move_lines_obj = self.env['account.move.line']
        for journal in journals:
            # cuenta por defecto de este diario
            account_id = journal.default_debit_account_id

            mlines = move_lines_obj.search([
                ('account_id', '=', account_id.id),
                ('date', '>=', data['date_from']),
                ('date', '<=', data['date_to']),
                ('journal_id', '=', journal.id)
            ])

            accum_balance = 0
            for line in mlines:
                accum_balance += line.balance

            # acumular el journal solo si tiene saldo
            if accum_balance:
                ret.append({
                    'journal': journal.name,
                    'total': accum_balance
                })
                total += accum_balance

        # acumular cuenta corriente si hay saldo residual
        if total_res:
            ret.append({
                'journal': CUENTA_CORRIENTE,
                'total': total_res
            })
            total += total_res

        return ret, total

    @api.multi
    def render_html(self, data):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))

        # buscar los journals que nay que reportar
        domain = [('cash_id', '=', data['form']['cash_id'])]
        journals = self.env['account.journal'].search(domain)

        invoices, total_inv, total_res = self._get_invoices(data['form'])
        journals, total_journal = self._get_journals(data['form'],
                                                     journals,
                                                     total_res)

        docargs = {
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'invoices': invoices,
            'total_invoiced': total_inv,
            'journals': journals,
            'total_journal': total_journal
        }

        return self.env['report'].render('account_cash_report.invoice_report',
                                         docargs)
