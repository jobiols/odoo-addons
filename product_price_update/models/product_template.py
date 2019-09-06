# For copyright and license notices, see __manifest__.py file in module root
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    vendor_price = fields.Monetary(
        'Coste de proveedor',
        compute="compute_vendor_price"
    )

    def compute_vendor_price(self):
        for rec in self:
            for seller in rec.seller_ids:
                rec.vendor_price = seller.price


    @api.model
    def add_fake_products(self):
        """ Agregar productos y vendors fake para testear la velocidad.
        """

        product_obj = self.env['product.template']
        rp_obj = self.env['res.partner']
        si_obj = self.env['product.supplierinfo']
        vendor = {
            'name': 'Vendor 0',
            'supplier': True
        }
        vendor_id = rp_obj.create(vendor)

        for x in range(1, 130000):
            product = {
                'name': 'Producto %d' % x,
                'default_code': 'p%d' % x,
                'standard_price': 10
            }
            tmpl_id = product_obj.create(product)
            print(product['name'])

            if x % 50 == 0:
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
