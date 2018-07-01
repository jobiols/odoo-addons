# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class Kpis(models.Model):
    _name = 'kpis_panel.kpis'

    vendor_id = fields.Many2one(
        'res.partner',
        domain="[('category_id.name', 'in', ['MERCADERIA'] )]",
        required=True,
    )
    total_payable = fields.Float(
        required=True,
    )
    stock_valuation = fields.Float(
        required=True,
        string="Stock valuation (sale price w/tax)"
    )
    count = fields.Integer(
        required=True,
    )

    @api.model
    @api.depends('vendor_id')
    def update(self):
        # limpiar la tabla
        self.search([]).unlink()
        # cargar todos los proveedores que tengan MERCADERIA
        domain = [('category_id.name', 'in', ['MERCADERIA'])]
        vendors = self.env['res.partner'].search(domain)
        for vendor in vendors:
            if not self.search([('id', '=', vendor.id)]):
                self.create({'vendor_id': vendor.id,
                             'total_payable': 0,
                             'stock_valuation': 0,
                             'count': 0})

        # miro la fecha de validez y me quedo con la mas nueva
        vendors = self.env['kpis_panel.kpis'].search([])
        for rec in vendors:
            _logger.info('Updating KPIS for {}'.format(rec.vendor_id.name))

            # obtener todos los productos que se le compran a este vendor y
            # que tienen stock >0
            domain = [('seller_ids.name', '=', rec.vendor_id.id),
                      ('virtual_available', '>', 0)]

            stock_valuation = count = 0
            stock = self.env['product.template'].search(domain)
            for prod in stock:

                # verifico si el producto tiene mas de un proveedor
                if len(prod.seller_ids) > 1:
                    # de los proveedores me quedo con el mas nuevo
                    ref = {'date': '0000-00-00', 'id': 0}
                    for seller in prod.seller_ids:
                        if seller.date_start > ref['date']:
                            ref['date'] = seller.date_start
                            ref['id'] = seller.name.id

                    # si el mas nuevo no coincide con el rec salteo y voy
                    # al siguiente
                    if ref['id'] != rec.vendor_id.id:
                        continue

                stock_valuation += prod.virtual_available * prod.final_price
                count += prod.virtual_available

            rec.write({
                'total_payable': rec.vendor_id.debit,
                'stock_valuation': stock_valuation,
                'count': count
            })
