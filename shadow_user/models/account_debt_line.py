# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _


class AccountDebtLine(models.Model):
    _inherit = "account.debt.line"

    white_journal = fields.Boolean(
        related="invoice_id.journal_id.white_journal",
        store=True,
        readonly=True
    )
