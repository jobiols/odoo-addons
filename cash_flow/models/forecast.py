# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _name = "cash_flow.forecast"

    forecast_date = fields.Date(
        readonly=True,
        states={'foreseen': [('readonly', False)]},
        index=True,
        help="Forecast date, it will be used in the cash flow",
        track_visibility='onchange'
    )

    amount = fields.Monetary(
        string='Forecasted amount',
        currency_field='currency_id',
        readonly=True,
        states={'foreseen': [('readonly', False)]},
        help="Total Forecasted amount without taxes",
        track_visibility='onchange'
    )
    description = fields.Char(

    )
    type = fields.Selection([
        ('out', 'Expenses Forecast'),
        ('in', 'Incomes Forecast')],
        help='Forecast type',
        track_visibility='onchange'
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        readonly=True,
        default=lambda self: self.env.user,
        track_visibility='onchange',
    )

    state = fields.Selection(
        [('foreseen', 'Foreseen'),
         ('invoiced', 'Invoiced')],
        string='Status',
        index=True,
        readonly=True,
        help='Forecast state',
        default='foreseen',
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
