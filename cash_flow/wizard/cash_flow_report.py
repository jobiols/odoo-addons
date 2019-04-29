# For copyright and license notices, see __manifest__.py file in module root

# from openerp import api,  fields, models, _
from openerp import models, fields, api
from datetime import date, timedelta


class CashFlowReport(models.TransientModel):
    _inherit = 'account.common.report'
    _name = "cash_flow_report"
    _description = "Cash Flow management and report"

    date_from = fields.Date(
        required=True,
        default=date.today().strftime('%Y-%m-%d')
    )
    date_to = fields.Date(
        required=True,
        default=(date.today() + timedelta(days=30)).strftime('%Y-%m-%d')
    )
    account_receivable_ids = fields.Many2many(
        required=True,
        comodel_name='account.account',
    )
    account_payable_ids = fields.Many2many(
        required=True,
        comodel_name='account.account',
    )
    account_cash_ids = fields.Many2many(
        required=True,
        comodel_name='account.account',
    )

    def _print_report(self, data):
        data['form'][
            'account_receivable_ids'] = self.account_receivable_ids.ids
        data['form']['account_payable_ids'] = self.account_payable_ids.ids
        data['form']['account_cash_ids'] = self.account_cash_ids.ids

        _action = 'cash_flow.action_cash_flow_report'
        return self.env.ref(_action).report_action(self, data)
