# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _name = "cash_flow.forecast"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Forecasts'

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
        track_visibility='onchange',
        required=True
    )
    description = fields.Text(

    )
    type = fields.Selection([
        ('out', 'Expenses Forecast'),
        ('in', 'Incomes Forecast')],
        readonly=True,
        states={'draft': [('readonly', False)],
                'foreseen': [('readonly', False)]},
        help='Forecast type',
        track_visibility='onchange',
        default='out'
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

    @api.multi
    def name_get(self):
        return [(fc.id, "%s - %s - %s" % (
            fc.forecast_date, fc.amount, fc.type)) for fc in self]
