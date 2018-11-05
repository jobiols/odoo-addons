# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from openerp import api, models
from datetime import datetime, timedelta

CUENTA_CORRIENTE = 'Cuenta Corriente'
EFECTIVO = 'Efectivo'


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
    def _get_journal_data(invoice):
        """ obtener una lista de diccionarios con los medios de pago con los
            que se pago esta factura
            cada diccionario tiene {journal_name, amount, date}
        """
        # tomo la lista de pagos del widget de la factura, y corrijo la
        # palabra false por False, esto pareceria javascript
        payments = invoice.payments_widget.replace('false', 'False')
        # le hago un eval para pasar ese texto a un diccionario
        payments = eval(payments)
        if payments:
            # aqui obtengo una lista de diccionarios c/u es un pago
            payments = payments['content']
            journals = []
            for payment in payments:
                jrnl = {
                    'journal_name': payment['journal_name'],
                    'date': payment['date'],
                    'amount': payment['amount']
                }
                # lo agrego sin repetir
                if jrnl not in journals:
                    journals.append(jrnl)

            if invoice.state == 'open':
                journals.append({
                    'journal_name': CUENTA_CORRIENTE,
                    'date': payment['date'],
                    'amount': invoice.residual
                })

            return journals

        return [{'journal_name': CUENTA_CORRIENTE}]

    def journal_names2journals(self, journal_names):
        """ Transformar la lista en un recordset, evitando CUENTA_CORRIENTE
        """
        journals = []
        for j in journal_names:
            if j['journal_name'] != CUENTA_CORRIENTE:
                journals.append(j['journal_name'])
        journal_obj = self.env['account.journal']
        return journal_obj.search([('name', 'in', journals)])

    def _get_invoices(self, data):
        """ Obtener todas las facturas / notas validadas que son out_
            (al cliente), y que estan en el periodo.
            No importa quien las valido.
        """
        domain = [
            ('date', '>=', data['date_from']),
            ('date', '<=', data['date_to']),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ]

        journals = set()
        invoice_obj = self.env['account.invoice']
        ret = []
        for invoice in invoice_obj.search(domain):
            # obtener un set con los medios de pago que pagaron la fac
            journal_data = self._get_journal_data(invoice)

            inv = {
                'number': invoice.display_name,
                'total': invoice.amount_total_signed,
                'journal': journal_data[0].get('journal_name', ''),
                'date': journal_data[0].get('date', ''),
                'paid': journal_data[0].get('amount', 0),
                'partner': invoice.partner_id.name,
                'salesperson': invoice.user_id.name
            }
            ret.append(inv)
            for jrnl in journal_data[1:]:
                inv = {
                    'number': '',
                    'total': 0,
                    'journal': jrnl.get('journal_name', ''),
                    'date': jrnl.get('date', ''),
                    'paid': jrnl.get('amount', 0),
                    'partner': '',
                    'salesperson': ''
                }
                ret.append(inv)

            journal_to_add_ids = self.journal_names2journals(journal_data)

            # agrego los ids a un set para evitar duplicados
            for journal in journal_to_add_ids:
                journals.add(journal.id)

        journal_obj = self.env['account.journal']
        return ret, journal_obj.search([('id', 'in', list(journals))])

    def _get_journals(self, data, journals, total_res):
        """ obtiene los medios de pago y el total acumulado en cada uno en
            el periodo considerado
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

    @staticmethod
    def get_total_res(invoices):
        """ Obtener el residual, o sea el total en cuenta corriente
        """
        res = 0
        for inv in invoices:
            if inv['journal'] == CUENTA_CORRIENTE:
                res += inv['paid']
        return res

    @staticmethod
    def get_total_inv(invoices):
        """ Obtener el total facturado
        """
        res = 0
        for inv in invoices:
            res += inv['total']
        return res

    @staticmethod
    def get_receipts(data):
        """ Obtener los recibos generados en esta caja

        """




        return [{
            'number': '001-00000054',
            'total': 123.23,
            'journal': 'Mercadopago Ventas',
            'invoice_no': 'FA-B 0001-00000548',
            'date': '2018-06-08',
            'partner': 'Daniel Diaz',
        }]

    @staticmethod
    def get_cash(data, invoices):
        """ Obtener el total de efectivo y fallo de caja
        """
        total_cash = 0
        for inv in invoices:
            if EFECTIVO in inv['journal']:
                total_cash += inv['total']

        return total_cash, data['cash_income'] - total_cash

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))

        invoices, journal_ids = self._get_invoices(data['form'])
        total_res = self.get_total_res(invoices)
        journals, total_journal = self._get_journals(
            data['form'], journal_ids, total_res)
        receipts = self.get_receipts(data['form'])
        total_invoiced = self.get_total_inv(invoices)
        total_income = 4564
        total_cash, cash_failure = self.get_cash(data['form'], invoices)


        docargs = {
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'invoices': invoices,
            'journals': journals,
            'receipts': receipts,
            'total_invoiced': total_invoiced,
            'total_income': total_income,
            'total_cash': total_cash,
            'cash_failure': cash_failure,
            'total_journal': total_journal
        }

        return self.env['report'].render('account_cash_report.invoice_report',
                                         docargs)
