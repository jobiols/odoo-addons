# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    price_by_supplier = fields.Float('Precio Proveedor')
    
    @api.multi
    def compute_price_by_supplier(self, supplier_id):
        if supplier_id > 0:
            for product in self:
                for supplier in product.seller_ids:
                    if supplier.name.id == supplier_id:
                        product.price_by_supplier = supplier.price
            self.env.cr.commit()
