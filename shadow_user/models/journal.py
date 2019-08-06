# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    white_journal = fields.Boolean(
        default=True
    )
