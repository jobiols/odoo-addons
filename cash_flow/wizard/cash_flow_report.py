# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

# from openerp import api,  fields, models, _
from openerp import models


class CashFlowReport(models.TransientModel):
    _name = "cash_flow_report"
    _description = "Cash Flow management and report"
