# -*- coding: utf-8 -*-

from openerp import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    cliente_defecto = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente Inicial',
        required=True
    )