# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, fields, models, _
import time


class AccountCashReport(models.TransientModel):
    _name = "cash.report"
    _description = "Accounting Cash Report"

    @api.model
    def _get_journals(self):
        return self.env['account.journal'].search([])

    chart_account_id = fields.Many2one(
        'account.account',
        'Plan de cuentas',
        help='Seleccione plan de cuentas',
        required=True,
        domain=[('parent_id', '=', False)]
    )
    period_from = fields.Many2one(
        'account.period',
        'Periodo inicial'
    )
    period_to = fields.Many2one(
        'account.period',
        'Periodo final'
    )
    filter = fields.Selection(
        [('filter_no', 'Sin filtro'),
         ('filter_date', 'Fecha'),
         ('filter_period', 'Periodos')],
        'Filtrado por',
        required=True,
        default='filter_date'
    )
    fiscalyear_id = fields.Many2one(
        'account.fiscalyear',
        'Año Fiscal',
        help='Dejarlo vacio para obtener todos los años fiscales abiertos',
    )
    amount_currency = fields.Boolean(
        'Con moneda',
        help='Agrega la columna moneda en el reporte si la moneda difiere de '
             'la moneda de la compañia.',
        default=False
    )
    initial_balance = fields.Boolean(
        string='Incluir balance inicial',
        help='Si selecciona el filtro por fecha o periodo, este campo le '
             'permite agregar una fila para mostrar el importe '
             'debe/haber/balance que precede al filtro que ha incluido.',
        default=True
    )
    sortby = fields.Selection(
        [('sort_date', 'Fecha'),
         ('sort_journal_partner', 'Diario & Partner')],
        string='Ordenado por',
        required=True,
        default='sort_date'
    )
    journal_ids = fields.Many2many(
        'account.journal',
        string='Journals',
        required=True,
        default=_get_journals
    )
    display_account = fields.Selection(
        [('all', 'Todas'),
         ('movement', 'Con movimientos'),
         ('not_zero', 'Con balance distinto de cero'), ],
        string='Mostrar cuentas',
        required=True,
        default='movement')
    only_cash_account = fields.Boolean(
        string='NO Incluir contrapartidas',
        default=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        readonly=True,
        default=lambda self: self.env.user.company_id
    )
    date_from = fields.Date(
        string='Fecha Inical',
        default=fields.Date.today()
    )
    date_to = fields.Date(
        string='Fecha Final',
        default=fields.Date.today()
    )
    target_move = fields.Selection(
        [('posted', 'Todos los asientos publicados'),
         ('all', 'Todos los asientos')],
        string='Movimientos destino',
        required=True,
        default='posted')
    expand_moves = fields.Boolean(
        'Expandir movimientos',
        default=False
    )

    @api.multi
    @api.constrains('expand_moves')
    def expand_moves_constraint(self):
        for rec in self:
            if not rec.expand_moves and not rec.only_cash_account:
                rec.only_cash_account = True

    @api.multi
    def pre_print_report(self, data):
        data['form'].update(self.read(['display_account'])[0])
        data['form'].update(self.read(['only_cash_account'])[0])
        data['form'].update(self.read(['expand_moves'])[0])
        return data

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(
            ['date_from', 'date_to', 'fiscalyear_id', 'journal_ids',
             'period_from', 'period_to',
             'filter', 'chart_account_id', 'target_move'])[0]
        for field in ['fiscalyear_id', 'chart_account_id', 'period_from',
                      'period_to']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]

        used_context = self._build_contexts(data)
        data['form']['periods'] = used_context.get('periods', False) and \
                                  used_context['periods'] or []
        data['form']['used_context'] = dict(used_context,
                                            lang=self.env.context.get('lang',
                                                                      'en_US'))
        return self._print_report(data)

    def _print_report(self, data):
        # import wdb;wdb.set_trace()
        data = self.pre_print_report(data)
        data['form'].update(self.read(
            ['expand_moves', 'only_cash_account', 'initial_balance',
             'amount_currency', 'sortby'])[0])
        records = self.env[data['model']].browse(data.get('ids', []))
        report_name = 'account_financial_cash_status.report_cash_status_template'
        landscape = data['form']['expand_moves']
        return self.env['report'].with_context(landscape=landscape).get_action(
            records, report_name, data=data)

    def _build_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form'][
            'journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form'][
            'target_move'] or ''
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        return result

    @api.one
    @api.onchange('chart_account_id')
    def onchange_chart_id(self):
        if not self.chart_account_id:
            self.chart_account_id = \
                self.env['account.account'].search([], limit=1)[0]

        company_id = self.env['account.account'].search(
            [('id', '=', self.chart_account_id.id)]).company_id

        now = time.strftime('%Y-%m-%d')
        domain = [('company_id', '=', company_id.id),
                  ('date_start', '<=', now), ('date_stop', '>=', now)]
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
                               LIMIT 1) AS period_stop''',
                             (fiscalyear_id, fiscalyear_id))
            periods = [i[0] for i in self._cr.fetchall()]
            if periods and len(periods) > 1:
                start_period = periods[0]
                end_period = periods[1]
            self.period_from = start_period
            self.period_to = end_period
            self.date_from = False
            self.date_to = False
