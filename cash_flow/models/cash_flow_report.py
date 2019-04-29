# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api
from datetime import datetime, timedelta

RECEIVABLE_ID = 1
PAYABLE_ID = 2
CASH_ID = 3


class CashFlowReport1(models.AbstractModel):
    _name = "report.cash_flow.cash_flow_report_template"
    _last_printed = (0.0, 0.0, 0.0)

    @staticmethod
    def inc_day(day):
        dt = datetime.strptime(day, '%Y-%m-%d')
        dt += timedelta(days=1)
        return datetime.strftime(dt, '%Y-%m-%d')

    def totalize(self, account, date):
        trial_balance = self.env['report.account.report_trialbalance']
        account_res = trial_balance.with_context(date_to=date)._get_accounts(
            account, 'movement')

        total = 0
        for account in account_res:
            total = account['balance']
        return total

    def printable(self, receivable, cash, payable):
        if receivable == 0 and cash == 0 and payable == 0:
            return False
        if (receivable, cash, payable) == self._last_printed:
            return False
        self._last_printed = (receivable, cash, payable)
        return True

    @api.multi
    def get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']

        domain = [('user_type_id', '=', RECEIVABLE_ID)]
        receivable_ids = self.env['account.account'].search(domain)

        domain = [('user_type_id', '=', PAYABLE_ID)]
        payable_ids = self.env['account.account'].search(domain)

        domain = [('user_type_id', '=', CASH_ID)]
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
            account_res = trial._get_accounts(cash_ids, 'movement')
            for account in account_res:
                cash += account['balance']

            payable = 0
            account_res = trial._get_accounts(payable_ids, 'movement')
            for account in account_res:
                payable -= account['balance']

            if self.printable(receivable, cash, payable):
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
