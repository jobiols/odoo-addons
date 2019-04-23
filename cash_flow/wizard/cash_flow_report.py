# For copyright and license notices, see __manifest__.py file in module root

# from openerp import api,  fields, models, _
from openerp import models, fields, api
from datetime import date, timedelta


class CashFlowReport(models.TransientModel):
    _name = "cash_flow_report"
    _description = "Cash Flow management and report"

    def _get_default_receivable_ids(self):
        return self.env['account.account'].search([('user_type_id', '=', 1)])

    def _get_default_payable_ids(self):
        return self.env['account.account'].search([('user_type_id', '=', 2)])

    def _get_default_cash_ids(self):
        return self.env['account.account'].search([('user_type_id', '=', 3)])

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
        default=_get_default_receivable_ids
    )
    account_payable_ids = fields.Many2many(
        required=True,
        comodel_name='account.account',
        default=_get_default_payable_ids
    )
    account_cash_ids = fields.Many2many(
        required=True,
        comodel_name='account.account',
        default=_get_default_cash_ids
    )

    def print_report(self):
        """ Imprimir el reporte
        """
        self.ensure_one()

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'account_receivable_ids': self.account_receivable_ids,
                'account_payable_ids': self.account_payable_ids,
                'account_cash_ids': self.account_cash_ids,
            }
        }

        _action = 'cash_flow.action_cash_flow'
        return self.env.ref(_action).report_action(self)
