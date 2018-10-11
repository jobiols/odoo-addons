# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        readonly=True,
        states={'draft': [('readonly', False)],
                'sent': [('readonly', False)]},
        help="The analytic account related to a purchase order.",
        copy=False
    )


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        related='order_id.analytic_account_id',
        store=True
    )
