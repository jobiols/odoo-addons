# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from openerp import api, models
from datetime import datetime, timedelta


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

    def _get_journal(self, invoice):
        return 'Efectivo'

    def _get_invoices(self, data):

        domain = [
            ('date', '>=', data['date_from']),
            ('date', '<=', data['date_to'])
        ]

        invoice_obj = self.env['account.invoice']
        ret = []
        total = 0
        for invoice in invoice_obj.search(domain):
            inv = {
                'number': invoice.display_name,
                'total': invoice.amount_total,
                'journal': self._get_journal(invoice),
                'partner': invoice.partner_id.name,
                'salesperson': invoice.user_id.name
            }
            total += invoice.amount_total
            ret.append(inv)

        return ret, total

        """
        [
                   {'number': 'FA-A 0001-00005487',
                    'total': 2133,
                    'journal': 'Efectivo',
                    'partner': 'efeca sa',
                    'salesperson': 'Gustavo'
                    },
                   {'number': 'FA-A 0001-00023424',
                    'total': 2324,
                    'journal': 'Tarjeta',
                    'partner': 'Liona sa',
                    'salesperson': 'Marcelo'
                    },
               ], 134144
        """

    def _get_journals(self, journals):
        return [{'journal': 'Efectivo',
                 'total': 200},
                {'journal': 'Tarjetas',
                 'total': 233},
                {'journal': 'Cuenta corriente',
                 'total': 23433},
                {'journal': 'Banco Galicia',
                 'total': 233243},
                ]

    @api.multi
    def render_html(self, data):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))

        # buscar los journals que nay que reportar
        domain = [('cash_id', '=', data['form']['cash_id'])]
        journals = self.env['account.journal'].search(domain)

        invoices, total_invoiced = self._get_invoices(data['form'])
        journals = self._get_journals(journals)

        docargs = {
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'invoices': invoices,
            'total_invoiced': total_invoiced,
            'journals': journals
        }

        # poner landscape si tengo rango de fechas
        # TODO no funciona el landscape.
        landscape = data['form']['date_range']
        return self.env['report'].with_context(landscape=landscape).render(
            'account_cash_report.invoice_report', docargs)
