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
             No importa quien las creo o quien las valido, tener en cuenta
             que si hay varias cajeras todas tendran las mismas facturas.

             Devuelve Lista con las facturas para el reporte y un recordset
             con los journals que se usarion en las facturas.
        """
        domain = [
            ('date', '>=', data['date_from']),
            ('date', '<=', data['date_to']),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ]

        invoice_obj = self.env['account.invoice']
        ret = []
        for invoice in invoice_obj.search(domain):
            # obtener una lista con los medios de pago que pagaron la fac
            journal_data = self._get_journal_data(invoice)

            # tener en cuenta que las facturas pueden venir en otra moneda.
            inv_c = invoice.currency_id
            comp_c = self.env.user.currency_id
            total = inv_c.compute(invoice.amount_total_signed, comp_c)

            # aca va la factura con el primer medio de pago
            inv = {
                'number': invoice.display_name,
                'total': total,
                'journal': journal_data[0].get('journal_name', ''),
                'date': journal_data[0].get('date', ''),
                'paid': journal_data[0].get('amount', 0),
                'partner': invoice.partner_id.name,
                'salesperson': invoice.user_id.name,
                'residual': invoice.residual
            }
            ret.append(inv)
            # aca van los demas medios de pago
            for jrnl in journal_data[1:]:
                inv = {
                    'number': '',
                    'total': 0,
                    'journal': jrnl.get('journal_name', ''),
                    'date': jrnl.get('date', ''),
                    'paid': jrnl.get('amount', 0),
                    'partner': '',
                    'salesperson': '',
                    'residual': 0
                }
                ret.append(inv)

        return ret

    def _get_journals(self, data, total_res, receipts):

        ret = {}
        for receipt in receipts:
            if receipt['journal'] != '':
                ret[receipt['journal']] = receipt['total'] + ret.get(
                    receipt['journal'], 0)

        journals = []
        for journ in ret:
            journals.append({
                'journal': journ,
                'total': ret[journ]
            })

        # acumular cuenta corriente si hay saldo residual
        if total_res:
            journals.append({
                'journal': CUENTA_CORRIENTE,
                'total': total_res
            })

        total = 0
        for kk in journals:
            total += kk['total']

        return journals, total

    @staticmethod
    def get_total_residual(invoices):
        """ Obtener el residual, o sea el total en cuenta corriente
        """
        res = 0
        for inv in invoices:
            if inv['journal'] == CUENTA_CORRIENTE:
                if inv['number']:
                    # si es una factura sumo el residual pero
                    res += inv['residual']
                else:
                    # si es pago parcial sumo el paid
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

    def get_receipts(self, data):
        """ Obtener los recibos generados en esta caja, y creados por esta
            cajera para este periodo.
        """
        ret = []
        total_income = 0
        payment_methods = set()

        # estos son los recibos que la cajera cobro en el periodo
        receipt_obj = self.env['account.payment.group']
        cashier_uid = data['cashier_uid']
        receipts = receipt_obj.search(
            [('create_uid', '=', cashier_uid),
             ('payment_date', '>=', data['date_from']),
             ('payment_date', '<=', data['date_to']),
             ('state', '=', 'posted')])

        for receipt in receipts:
            # por si hay un pago sin factura asociada
            if receipt.matched_move_line_ids:
                invoice_no = receipt.matched_move_line_ids[
                    0].move_id.display_name
            else:
                invoice_no = False
            ret.append({
                'number': receipt.name,
                'total': receipt.payments_amount,
                'journal': '',
                'invoice_no': invoice_no,
                'date': receipt.payment_date,
                'partner': receipt.partner_id.name,
            })
            total_income += receipt.payments_amount

            for invoice in receipt.matched_move_line_ids[1:]:
                ret.append({
                    'number': '',
                    'total': 0,
                    'journal': '',
                    'invoice_no': invoice.move_id.display_name,
                    'date': '',
                    'partner': '',
                })

            for payment_method in receipt.payment_ids:
                payment_methods.add(payment_method.journal_id.id)
                ret.append({
                    'number': '',
                    'total': payment_method.amount,
                    'journal': payment_method.journal_id.name,
                    'invoice_no': '',
                    'date': '',
                    'partner': '',
                })

        return ret, total_income

    @staticmethod
    def get_cash(data, receipts):
        """ Obtener el total de efectivo y fallo de caja
        """
        total_cash = 0
        for inv in receipts:
            if EFECTIVO in inv['journal']:
                total_cash += inv['total']

        return total_cash, data['cash_income'] - total_cash

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))

        # lista con las facturas y los journals relacionados
        invoices = self._get_invoices(data['form'])

        # suma el total residual (cuenta corriente)
        total_res = self.get_total_residual(invoices)

        receipts, total_income = self.get_receipts(data['form'])

        journals, total_journal = self._get_journals(data['form'], total_res,
                                                     receipts)
        total_invoiced = self.get_total_inv(invoices)
        total_cash, cash_failure = self.get_cash(data['form'], receipts)

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
            'total_residual': total_res,
            'cash_failure': cash_failure,
            'total_journal': total_journal
        }

        return self.env['report'].render('account_cash_report.invoice_report',
                                         docargs)
