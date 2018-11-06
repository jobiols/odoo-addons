# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, _
import time


class InvoiceReport(models.TransientModel):
    _inherit = "account.common.report"
    _name = "account_cash_report.invoice.report"
    _description = "Invoice Report"

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
    cash_income = fields.Float(

    )

    def _print_report(self, data):
        # no tenemos en cuenta lo que viene en data, le ponemos los datos aca.

        users_obj = self.env['res.users']
        cashier_id = users_obj.search([('cash_id', '=', self.cash_id.id)])
        data = {
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'date_range': self.date_from != self.date_to,
                'cash_income': self.cash_income,
                'title': _('Invoice report'),
                'cash_id': self.cash_id.id,
                'cashier_uid': cashier_id.id,
                'cash': self.cash_id.name,
            }
        }

        return self.env['report'].get_action(
            self, 'account_cash_report.invoice_report', data=data)
