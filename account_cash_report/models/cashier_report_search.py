# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from openerp import api, models
from datetime import datetime, timedelta


class ReportCashier(models.AbstractModel):
    _name = 'report.account_cash_report.cashier_report'

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

    def _get_account_move_entry(self, data, journals):
        """
        :param:
                journals: the recordset of journals

        Returns a list of dictionaries each one is a jounral and all the moves
         with following key and value {
            'journal': 'ARGENCARD Ventas',
            'balance': 123456.4545,
            'lines': [
                {
                    'date': '2018-05-02',
                    'partner_name': u'Juan de los palotes'
                    'lref': None,
                    'move_name': u'VEN01/2018/0001',
                    'balance': 2089.64,
                },
        }
        """
        # import wdb; wdb.set_trace()

        ret = []
        move_lines_obj = self.env['account.move.line']
        for journal in journals:
            jour = {}
            # cuenta por defecto de este diario
            account_id = journal.default_debit_account_id

            mlines = move_lines_obj.search([
                ('account_id', '=', account_id.id),
                ('date', '>=', data['date_from']),
                ('date', '<=', data['date_to']),
                ('journal_id', '=', journal.id)
            ])

            lines = []
            if journal.initial_balance:
                accum_balance = self.initial_balance(account_id,
                                                     data['date_to'])
                if data['expand_moves']:
                    lin = {}
                    lin['date'] = data['date_from']
                    lin['partner_name'] = ''
                    lin['ref'] = 'Balance Inicial'
                    lin['move_name'] = ''
                    lin['balance'] = accum_balance
                    lines.append(lin)
            else:
                accum_balance = 0

            for line in mlines:
                display_names = []
                if line.payment_id and line.payment_id.payment_group_id:
                    for mml in line.payment_id.payment_group_id.matched_move_line_ids:  #noqa
                        display_names.append(mml.move_id.display_name)

                display_name = ', '.join(display_names)

                lin = {}
                accum_balance += line.balance
                if data['expand_moves']:
                    lin['date'] = line.date
                    lin['partner_name'] = line.partner_id.name
                    lin['ref'] = line.ref or '/'
                    lin['move_name'] = display_name if display_name else line.move_id.display_name #noqa
                    lin['balance'] = line.balance
                    lines.append(lin)

            jour['journal'] = journal.name
            jour['balance'] = accum_balance
            jour['lines'] = lines

            # acumular el journal solo si tiene saldo
            if accum_balance:
                ret.append(jour)

        return ret

    @api.multi
    def render_html(self, data):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))

        # buscar los journals que nay que reportar
        domain = [('cash_id', '=', data['form']['cash_id'])]
        journals = self.env['account.journal'].search(domain)
        accounts_res = self._get_account_move_entry(data['form'], journals)

        docargs = {
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'journals': accounts_res,
        }

        # poner landscape si tengo rango de fechas
        # TODO no funciona el landscape.
        landscape = data['form']['date_range']
        return self.env['report'].with_context(landscape=landscape).render(
            'account_cash_report.cashier_report', docargs)
