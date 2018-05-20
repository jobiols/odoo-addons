# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from openerp import api, models


class ReportCashier(models.AbstractModel):
    _name = 'report.account_cash_report.cashier_report'

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
                    'ldate': '2018-05-02',
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
            balance = 0
            # cuenta por defecto de este diario
            account_id = journal.default_debit_account_id
            print journal.name
            mlines = move_lines_obj.search(
                    [('account_id', '=', account_id.id)])

            lines = []
            for line in mlines:
                lin = {}
                #print '{} / {:30} / [{:20}] / [{}] C={:7.2f} D={:7.2f} B={:7.2f} [{}] {}'.format(line.date, line.partner_id.name, line.name, line.ref,
                #         line.credit, line.debit, line.balance, line.narration,
                #         line.account_id.name                )
                balance += line.balance
                lin['ldate'] = line.date
                lin['partner_name'] = line.partner_id.name
                lin['ref'] = line.ref or '/'
                lin['move_name'] = line.name
                lin['balance'] = line.balance
                lines.append(lin)

            jour['journal'] = journal.name
            jour['balance'] = balance
            jour['lines'] = lines
            ret.append(jour)

        #import pprint
        #pp = pprint.PrettyPrinter()
        #pp.pprint(ret)

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

        #import wdb;wdb.set_trace()

        docargs = {
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'journals': accounts_res,
        }
        return self.env['report'].render('account_cash_report.cashier_report',
                                         docargs)
