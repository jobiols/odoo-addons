# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, api, models, _
from openerp.exceptions import UserError

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models, _
from openerp.exceptions import UserError


class CashierReport(models.TransientModel):
    _inherit = "account.common.report"
    _name = "account_cash_report.cashier.report"
    _description = "Cashier Report"

    cash_id = fields.Many2one(
            'account_cash_report.cash',
            required=True,
            string="Cash"
    )

    date_from = fields.Date(
            default=lambda *a: time.strftime('%Y-%m-%d')
    )
    date_to = fields.Date(
            default=lambda *a: time.strftime('%Y-%m-%d')
    )
    expand_moves = fields.Boolean(
            default=False,
            help="Show account movements"
    )

    def _print_report(self, data):
        # no tenemos en cuenta lo que viene en data, le ponemos los datos aca.
        data = {
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'date_range': (self.date_from != self.date_to) and self.expand_moves,
                'title': 'Reporte de caja',
                'expand_moves': self.expand_moves,
                'cash_id': self.cash_id.id,
                'cash': self.cash_id.name
            }
        }

        return self.env['report'].get_action(
                self, 'account_cash_report.cashier_report', data=data)
