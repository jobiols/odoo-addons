# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging

_log = logging.getLogger("==== PRODUCT PRICE SUPPLIER ====")


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    price_by_supplier = fields.Float('Precio Proveedor')
    
    @api.multi
    def compute_price_by_supplier(self, supplier_id):
        _log.info("El proveedor es: %s" % supplier_id)
        if supplier_id > 0:
            for product in self:
                for supplier in product.seller_ids:
                    if supplier.name.id == supplier_id:
                        product.price_by_supplier = supplier.price
            self.env.cr.commit()


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def add_fake_products(self):
        """ Agregar productos fake para testear la velocidad.
        """

        product_obj = self.env['product.template']
        rp_obj = self.env['res.partner']
        si_obj = self.env['product.supplierinfo']

        for x in range(1, 40000):
            product = {
                'name': 'Producto %d' % x,
                'default_code': 'p%d' % x,
                'type': 'product',
                'standard_price': 10
            }
            tmpl_id = product_obj.create(product)
            print(product['name'])

            vendor = {
                'name': 'Vendor %d' % x,
                'supplier': True
            }
            vendor_id = rp_obj.create(vendor)

            si_obj.create({
                'name': vendor_id.id,
                'price': product['standard_price'],
                'product_tmpl_id': tmpl_id.id
            })
