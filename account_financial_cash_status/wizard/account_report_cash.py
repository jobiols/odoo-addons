# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, fields, models, _


class AccountCashReport(models.TransientModel):
    _inherit = "account.report.general.ledger"
    _name = "cash.report"
    _description = "Accounting Cash Report"

    """
    @api.multi
    def check_report(self):
        super(AccountCashReport, self).check_report()

    @api.multi
    def _print_report(self, data):
        print ' bbbbbbbbbbbbbbb', data

        data['form'].update(self.read(['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp',
                                       'account_report_id', 'enable_filter', 'label_filter', 'target_move'])[0])
        return self.env['report'].get_action(self, 'account_financial_cash_status.report_cash_status_template',
                                             data=data)
    """

    def _print_report(self, data):
        print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        data = self.pre_print_report(data)
        data['form'].update(self.read(['initial_balance', 'sortby'])[0])
        if data['form'].get('initial_balance') and not data['form'].get('date_from'):
            raise UserError(_("You must define a Start Date"))
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].with_context(landscape=True).get_action(records, 'account_financial_cash_status.report_cash_status_template', data=data)
