# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Esta es la caja que es responsabilidad de esta cajera
    cash_id = fields.Many2one(
        'account_cash_report.cash',
        string="Cash"
    )
