# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from openerp import api, models, fields


class Cash(models.AbstractModel):
    _name = 'account_cash_report.cash'

    name = fields.Char(
        help="Name of this Cash"
    )

    journal_ids = fields.One2many(

    )