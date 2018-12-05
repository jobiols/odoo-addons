# -*- coding: utf-8 -*-

from openerp import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_fiscal = fields.Boolean(
        string=u"Punto FISCAL"
    )
    dir_fiscal = fields.Char(
        string=u"Directorio Fiscal",
        size=60,
        default="/opt/odoo/extra-addons/avalon/fiscal/Pto01/"
    )
    diario_fiscal = fields.Many2one(
        'pos.config',
        string="Diario Fiscal"
    )
