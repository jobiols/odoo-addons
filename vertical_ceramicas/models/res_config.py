# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class PricelistConfiguration(models.TransientModel):
    _name = 'prices.config.settings'
    _inherit = 'res.config.settings'

    pricelist_1 = fields.Many2one(
        'product.pricelist',
        'Precio 1',
        help='Permite seleccionar la lista de precios para el precio 1'
    )
    pricelist_2 = fields.Many2one(
        'product.pricelist',
        'Precio 2',
        help='Permite seleccionar la lista de precios para el precio 2'
    )
    pricelist_3 = fields.Many2one(
        'product.pricelist',
        'Precio 3',
        help='Permite seleccionar la lista de precios para el precio 3'
    )

    #    default_test = fields.Char('test',
    # default_model='prices.config.settings')

    @api.model
    def get_default_pricelist_1(self, fields):
        confs = self.env['prices.config.settings'].search([], limit=1,
                                                          order="id desc")
        return {'pricelist_1': confs.pricelist_1.id}

    @api.model
    def get_default_pricelist_2(self, fields):
        confs = self.env['prices.config.settings'].search([], limit=1,
                                                          order="id desc")
        return {'pricelist_2': confs.pricelist_2.id}

    @api.model
    def get_default_pricelist_3(self, fields):
        confs = self.env['prices.config.settings'].search([], limit=1,
                                                          order="id desc")
        return {'pricelist_3': confs.pricelist_3.id}
