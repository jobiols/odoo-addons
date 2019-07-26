# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _name = "cash_flow.forecast"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Forecasts'
    _order = 'forecast_date desc'

    forecast_date = fields.Date(
        readonly=True,
        states={'draft': [('readonly', False)],
                'foreseen': [('readonly', False)]},
        index=True,
        help="Forecast date, it will be used in the cash flow",
        track_visibility='onchange',
        required=True
    )
    amount = fields.Monetary(
        string='Forecasted amount',
        currency_field='currency_id',
        readonly=True,
        states={'draft': [('readonly', False)],
                'foreseen': [('readonly', False)]},
        help="Total Forecasted amount without taxes",
        required=True
    )
    expense_forecast = fields.Monetary(
        compute="_compute_expense_forecast",
        track_visibility='onchange',
    )
    revenue_forecast = fields.Monetary(
        compute="_compute_expense_forecast",
        track_visibility='onchange',
    )
    description = fields.Text(

    )
    tree_description = fields.Char(
        compute="_compute_tree_description"
    )
    type = fields.Selection([
        ('expenses', 'Expenses Forecast'),
        ('incomes', 'Incomes Forecast')],
        readonly=True,
        states={'draft': [('readonly', False)],
                'foreseen': [('readonly', False)]},
        help='Forecast type',
        track_visibility='onchange',
        default='expenses'
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        readonly=True,
        states={'draft': [('readonly', False)],
                'foreseen': [('readonly', False)]},
        default=lambda self: self.env.user,
        track_visibility='onchange',
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('foreseen', 'Foreseen'),
         ('invoiced', 'Invoiced')],
        string='Status',
        index=True,
        readonly=True,
        help='Forecast state',
        default='draft',
        track_visibility='onchange',
    )

    def _compute_expense_forecast(self):
        for rec in self:
            if rec.type == 'expenses':
                rec.expense_forecast = rec.amount
                rec.revenue_forecast = 0
            else:
                rec.expense_forecast = 0
                rec.revenue_forecast = rec.amount

    def _compute_tree_description(self):
        for rec in self:
            if rec.description:
                elipsis = '...' if len(rec.description) > 50 else ''
                rec.tree_description = rec.description[:50] + elipsis

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        readonly=True,
        states={'foreseen': [('readonly', False)]},
        default=_default_currency,
        track_visibility='always')

    def name_get(self):
        return [(fc.id, "%s - %s - %s" % (
            fc.forecast_date, fc.amount, fc.type)) for fc in self]

    def validate(self):
        for rec in self:
            rec.state = 'foreseen'

    def go_invoiced(self):
        for rec in self:
            rec.state = 'invoiced'
