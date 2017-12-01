# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, fields, models, _


class AccountCashReport(models.TransientModel):
    _name = "cash.report"
    _description = "Accounting Cash Report"

    initial_balance = fields.Boolean(
            string='Include Initial Balances',
            help='If you selected date, this field allow you to add a row to display the amount of debit/credit/balance that precedes the filter you\'ve set.'
    )
    sortby = fields.Selection(
            [('sort_date', 'Date'),
             ('sort_journal_partner', 'Journal & Partner')],
            string='Sort by',
            required=True,
            default='sort_date'
    )
    journal_ids = fields.Many2many(
            'account.journal',
            'account_report_general_ledger_journal_rel',
            'account_id',
            'journal_id',
            string='Journals',
            required=True
    )
    display_account = fields.Selection(
            [('all', 'All'),
             ('movement', 'With movements'),
             ('not_zero', 'With balance is not equal to 0'), ],
            string='Display Accounts',
            required=True,
            default='movement')
    company_id = fields.Many2one(
            'res.company',
            string='Company',
            readonly=True,
            default=lambda self: self.env.user.company_id
    )
    journal_ids = fields.Many2many(
            'account.journal',
            string='Journals',
            required=True,
            default=lambda self: self.env['account.journal'].search([])
    )
    date_from = fields.Date(
            string='Start Date'
    )
    date_to = fields.Date(
            string='End Date'
    )
    target_move = fields.Selection(
            [('posted', 'All Posted Entries'),
             ('all', 'All Entries')],
            string='Target Moves',
            required=True,
            default='posted')

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update(self.read(['initial_balance', 'sortby'])[0])
        if data['form'].get('initial_balance') and not data['form'].get('date_from'):
            raise UserError(_("You must define a Start Date"))
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].with_context(landscape=True).get_action(records, 'account.report_generalledger',
                                                                          data=data)

    @api.multi
    def pre_print_report(self, data):
        data['form'].update(self.read(['display_account'])[0])
        return data

    def _build_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        return result

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)
