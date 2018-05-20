# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, models, fields


class Cash(models.Model):
    _name = 'account_cash_report.cash'

    name = fields.Char(
        help="Name of this Cash"
    )

    journal_ids = fields.One2many(
        comodel_name="account.journal",
        inverse_name="cash_id",
        string="Journals"
    )
