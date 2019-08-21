# Copyright 2014-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError


class Settlement(models.Model):
    _inherit = "sale.commission.settlement"

    def _prepare_invoice_header(self, settlement, journal, date=False):
        invoice = self.env['account.invoice'].new({
            'partner_id': settlement.agent.id,
            'type': ('in_invoice' if journal.type == 'purchase' else
                     'in_refund'),
            'date_invoice': date,
            'journal_id': journal.id,
            'company_id': settlement.company_id.id,
            'state': 'draft',
            'currency_id': settlement.company_id.currency_id.id
        })
        # Get other invoice values from onchanges
        invoice._onchange_partner_id()
        invoice._onchange_journal_id()
        return invoice._convert_to_write(invoice._cache)
