# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    payment_term_id = fields.Many2one(
        required=False
    )
