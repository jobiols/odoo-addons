# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, fields, models, _
import time


class AccountCashReport(models.TransientModel):
    _name = "cash_report"
    _description = "Accounting Cash Report"

    chart_account_id = fields.Many2one(
            'account.account',
            'Chart of Account',
            help='Select Charts of Accounts',
            required=True,
            domain=[('parent_id', '=', False)]
    )
    period_from = fields.Many2one(
            'account.period',
            'Start Period'
    )
    period_to = fields.Many2one(
            'account.period',
            'End Period'
    )
    filter = fields.Selection(
            [('filter_no', 'No Filters'),
             ('filter_date', 'Date'),
             ('filter_period', 'Periods')],
            "Filter by",
            required=True,
            default="filter_date"
    )
    fiscalyear_id = fields.Many2one(
            'account.fiscalyear',
            'Fiscal Year',
            help='Keep empty for all open fiscal year',
    )
    amount_currency = fields.Boolean(
            "With Currency",
            help="It adds the currency column on report if the currency differs from the company currency."
    )
    landscape = fields.Boolean(
            "Landscape Mode"
    )
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
            string='Journals',
            required=True,
            default=lambda self: self.env['account.journal'].search([])
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
    date_from = fields.Date(
            string='Start Date',
#            default=fields.Date.today()
            default='2017-11-01'
    )
    date_to = fields.Date(
            string='End Date',
            default='2017-11-01'
#            default=fields.Date.today()
    )
    target_move = fields.Selection(
            [('posted', 'All Posted Entries'),
             ('all', 'All Entries')],
            string='Target Moves',
            required=True,
            default='posted')

    @api.multi
    def pre_print_report(self, data):
        data['form'].update(self.read(['display_account'])[0])
        return data

    # -----------------------------------------------------

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'fiscalyear_id', 'journal_ids', 'period_from', 'period_to',
                                  'filter', 'chart_account_id', 'target_move'])[0]
        for field in ['fiscalyear_id', 'chart_account_id', 'period_from', 'period_to']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]

        used_context = self._build_contexts(data)
        data['form']['periods'] = used_context.get('periods', False) and used_context['periods'] or []
        data['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang', 'en_US'))
        return self._print_report(data)

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update(self.read(['landscape', 'initial_balance', 'amount_currency', 'sortby'])[0])
        records = self.env[data['model']].browse(data.get('ids', []))
        report_name = 'account_financial_cash_status.report_cash_status_template'
#        report_name = 'account.report_generalledger'
        return self.env['report'].with_context(landscape=True).get_action(records, report_name, data=data)

    def _build_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        return result

    @api.one
    @api.onchange('chart_account_id')
    def onchange_chart_id(self):
        if not self.chart_account_id:
            self.chart_account_id = self.env['account.account'].search([], limit=1)[0]

        company_id = self.env['account.account'].search([('id', '=', self.chart_account_id.id)]).company_id

        now = time.strftime('%Y-%m-%d')
        domain = [('company_id', '=', company_id.id), ('date_start', '<=', now), ('date_stop', '>=', now)]
        fiscalyears = self.env['account.fiscalyear'].search(domain, limit=1)

        self.company_id = company_id
        self.fiscalyear_id = fiscalyears and fiscalyears[0] or False

    @api.one
    @api.onchange('filter')
    def onchange_filter(self):
        res = {'value': {}}
        if self.filter == 'filter_no':
            self.period_from = False
            self.period_to = False
            self.date_from = False
            self.date_to = False
        if filter == 'filter_date':
            self.period_from = False
            self.period_to = False
            self.date_from = time.strftime('%Y-01-01')
            self.date_to = time.strftime('%Y-%m-%d')
        if filter == 'filter_period' and fiscalyear_id:
            start_period = end_period = False
            self._cr.execute('''
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.special = false
                               ORDER BY p.date_start ASC, p.special ASC
                               LIMIT 1) AS period_start
                UNION ALL
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.date_start < NOW()
                               AND p.special = false
                               ORDER BY p.date_stop DESC
                               LIMIT 1) AS period_stop''', (fiscalyear_id, fiscalyear_id))
            periods = [i[0] for i in self._cr.fetchall()]
            if periods and len(periods) > 1:
                start_period = periods[0]
                end_period = periods[1]
            self.period_from = start_period
            self.period_to = end_period
            self.date_from = False
            self.date_to = False
