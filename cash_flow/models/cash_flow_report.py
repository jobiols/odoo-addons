# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api
from datetime import datetime, timedelta


class CashFlowReport1(models.AbstractModel):
    _name = "report.cash_flow.cash_flow_report_template"

    @staticmethod
    def inc_day(day):
        dt = datetime.strptime(day, '%Y-%m-%d')
        dt += timedelta(days=1)
        return datetime.strftime(dt, '%Y-%m-%d')

    def totalize(self, account, date):
        trial_balance = self.env['report.account.report_trialbalance']
        account_res = trial_balance.with_context(date_to=date)._get_accounts(account, 'movement')

        total = 0
        for account in account_res:
            total = account['balance']
        return total

    @api.multi
    def get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']

        domain = [('user_type_id', '=', 1)]
        receivable_ids = self.env['account.account'].search(domain)

        domain = [('user_type_id', '=', 2)]
        payable_ids = self.env['account.account'].search(domain)

        domain = [('user_type_id', '=', 2)]
        cash_ids = self.env['account.account'].search(domain)

        docs = []
        trial_balance = self.env['report.account.report_trialbalance']
        while date_from <= date_to:

            trial = trial_balance.with_context(date_to=date_from)
            receivable = 0
            account_res = trial._get_accounts(receivable_ids, 'movement')
            for account in account_res:
                receivable += account['balance']

            cash = 0
            account_res = trial._get_accounts(payable_ids, 'movement')
            for account in account_res:
                cash += account['balance']

            payable = 0
            account_res = trial._get_accounts(cash_ids, 'movement')
            for account in account_res:
                payable += account['balance']

            if receivable != 0 or cash != 0 or payable != 0:
                docs.append({
                    'date': date_from,
                    'receivable': receivable,
                    'cash': cash,
                    'payable': payable,
                    'total': receivable + cash - payable},
                )

            date_from = self.inc_day(date_from)

        return {
            'docs': docs,
        }
