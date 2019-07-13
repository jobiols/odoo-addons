# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class AccountInvoice(models.Model):
    _name = "cash_flow.forecast"

    forecast_date = fields.Date(
        readonly=True,
        states={'foreseen': [('readonly', False)]},
        index=True,
        help="Forecast date, it will be used in the cash flow",
        copy=False,
        track_visibility='always'
    )

    state = fields.Selection([
        ('foreseen', 'Foreseen'),
        ('invoiced', 'Invoiced')],
        help='Forecast state',
        track_visibility='always'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        readonly=True,
        states={'foreseen': [('readonly', False)]},
        track_visibility='always'
    )

    amount = fields.Monetary(
        string='Forecasted amount',
        currency_field='currency_id',
        store=True, readonly=True,
        compute='_compute_amount',
        help="Total Forecasted amount without taxes",
        track_visibility='always'
    )

    type = fields.Selection([
        ('out', 'Expenses Forecast'),
        ('in', 'Incomes Forecast')],
        help='Forecast type',
        track_visibility='always'
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        track_visibility='onchange',
        readonly=True,
        default=lambda self: self.env.user,
        copy=False
    )
