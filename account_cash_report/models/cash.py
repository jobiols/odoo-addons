# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from openerp import api, models


class Cash(models.AbstractModel):
    _name = 'account_cashier_report.cash'
