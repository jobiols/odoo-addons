# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api

PARAMS = [
    ("pricelist_1", 'pricelist_1'),
    ("pricelist_2", 'pricelist_2'),
    ("pricelist_3", 'pricelist_3'),
]


class PricelistConfiguration(models.TransientModel):
    _inherit = 'sale.config.settings'

    pricelist_1 = fields.Many2one(
        'product.pricelist',
        'Precio 1',
        help='Permite seleccionar la lista de precios para el precio 1',
    )
    pricelist_2 = fields.Many2one(
        'product.pricelist',
        'Precio 2',
        help='Permite seleccionar la lista de precios para el precio 2',
    )
    pricelist_3 = fields.Many2one(
        'product.pricelist',
        'Precio 3',
        help='Permite seleccionar la lista de precios para el precio 3',
    )

    @api.multi
    def set_params(self):
        self.ensure_one()
        for field_name, key_name in PARAMS:
            value = getattr(self, field_name, '').id
            self.env['ir.config_parameter'].set_param(key_name, value)

    @api.multi
    def get_default_params(self, fields):
        res = dict()
        for field_name, key_name in PARAMS:
            value = self.env['ir.config_parameter'].get_param(key_name, False)
            res[field_name] = int(value)
        return res
