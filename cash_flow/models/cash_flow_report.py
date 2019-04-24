# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

from openerp import models, fields, api
from datetime import date, timedelta


class CashFlowReport1(models.AbstractModel):
    _name = "report.cash_flow.cash_flow_report_template"

    @api.multi
    def get_report_values(self, docids, data=None):
        import wdb;wdb.set_trace()
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        account_receivable_ids = data['form']['account_receivable_ids']
        account_payable_ids = data['form']['account_payable_ids']
        account_cash_ids = data['form']['account_cash_ids']




        docs = [
            {'date': '10/11/2019',
             'receivable': 13414,
             'cash': 11231,
             'payable': 14313,
             'total': 34334},
            {'date': '10/11/2019',
             'receivable': 13414,
             'cash': 11231,
             'payable': 14313,
             'total': 34334},
            {'date': '10/11/2019',
             'receivable': 13414,
             'cash': 11231,
             'payable': 14313,
             'total': 34334},
            {'date': '10/11/2019',
             'receivable': 13414,
             'cash': 11231,
             'payable': 14313,
             'total': 34334},
        ]

        return {
            'docs': docs,
        }
