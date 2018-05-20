# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import fields, models, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    cash_id = fields.Many2one(
        'account_cash_report.cash',
        string="Cash"
    )
