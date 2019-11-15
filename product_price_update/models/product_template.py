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
