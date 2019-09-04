# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import Warning

import logging

_logger = logging.getLogger("..:: PRICE UPDATE ::..")


class ProductPriceUpdate(models.TransientModel):
    _name = 'product.price.update'

    name = fields.Many2one('pos.category', 'Categoría', required=True)
    type = fields.Selection([
        ('percent', 'Porcentaje'),
        ('amount', 'Monto')
    ], "Tipo de actualización", default = 'percent', required=True)
    price = fields.Selection([
        ('sale', 'De venta'),
        ('purchase', 'De compra'),
        ('supplier_purchase', 'De compra con proveedor')
    ], "Actualizar Precio", default='sale', required=True)
    supplier = fields.Many2one('res.partner', 'Proveedor')
    product_ids = fields.Many2many('product.product', string='Productos a afectar')
    product_ids_2 = fields.Many2many('product.product', string='Productos a afectar')
    value = fields.Float("Valor", required=True)
    
    @api.multi
    @api.onchange('name', 'price', 'supplier')
    def change_products(self):
        domain = []
        if self.name:
            domain = domain + [('pos_categ_id', '=', self.name.id)]
        if self.price == 'supplier_purchase' and self.supplier:
            self.with_context(supplier_id=self.supplier.id)
            domain = domain + [('seller_ids.name', 'in', [self.supplier.id])]
        if len(domain) > 0:
            self.product_ids = self.env['product.product'].search(domain)
            self.product_ids_2 = self.env['product.product'].search(domain)
        if self.supplier:
            self.product_ids_2.compute_price_by_supplier(self.supplier.id)
 
    def confirm(self):
        self.change_products()
        product_ids = self.product_ids if len(self.product_ids) > 0 else self.product_ids_2
        if len(product_ids) <= 0:
            raise Warning("Ningún producto será afectado, por favor modifique los criterios.")
        for p in product_ids:
            if self.price == 'sale':
                if self.type == 'percent':
                    p.lst_price = p.lst_price + (p.lst_price*self.value/100.0)
                elif self.type == 'amount':
                    p.lst_price = p.lst_price + self.value
            if self.price == 'purchase':
                if self.type == 'percent':
                    p.standard_price = p.standard_price + (p.standard_price*self.value/100.0)
                elif self.type == 'amount':
                    p.standard_price = p.standard_price + self.value
            if self.price == 'supplier_purchase':
                if self.type == 'percent':
                    for supplier in p.seller_ids:
                        if supplier.name.id == self.supplier.id:
                            supplier.price = supplier.price + (supplier.price*self.value/100.0)
                elif self.type == 'amount':
                    for supplier in p.seller_ids:
                        if supplier.name.id == self.supplier.id:
                            supplier.price = supplier.price + self.value
        self.env.cr.commit()
        return {
            'name': 'Actualizar Precios',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.price.update',
            'target':'new',
            'context':{
                'default_name': self.name.id,
                'default_type': self.type,
                'default_price': self.price,
                'default_supplier': self.supplier.id,
                'default_value': 0
            } 
        }
