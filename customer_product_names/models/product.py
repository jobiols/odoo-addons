# For copyright and license notices, see __manifest__.py file in module root

from odoo import api, fields, models, tools, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    customer_ids = fields.One2many(
        'product.customerinfo',
        'product_tmpl_id',
        'Customers'
    )
    variant_customer_ids = fields.One2many(
        'product.customerinfo',
        'product_tmpl_id'
    )


class CustomerInfo(models.Model):
    _name = "product.customerinfo"
    _description = "Information about the customer product name"
    _sql_constraints = [
        ('customer_uniq',
         'unique (name, product_code, company_id)',
         'There must be only one code for each customer and company !'),
    ]

    name = fields.Many2one(
        'res.partner', 'Customer',
        domain=[('customer', '=', True)],
        ondelete='cascade', required=True,
        help="Customer for this product"
    )
    product_name = fields.Char(
        'Customer Product Name',
        help="This customer's product name will be used when printing a "
             "quotation.",
        required=True
    )
    product_code = fields.Char(
        'Customer Product Code',
        help="This customer's product code will be used when printing a "
             "quotation.",
        required=True
    )
    product_uom = fields.Many2one(
        'product.uom',
        'Customer Unit of Measure',
        readonly="1",
        related='product_tmpl_id.uom_po_id',
        help="This comes from the product form."
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id.id,
        index=1
    )
    date_start = fields.Date(
        'Start Date',
        help="Start date for this customer name"
    )
    date_end = fields.Date(
        'End Date',
        help="End date for this customer name"
    )
    product_id = fields.Many2one(
        'product.product',
        'Product Variant',
        help="If not set, the customer name will apply to all variants "
             "of this products."
    )
    product_tmpl_id = fields.Many2one(
        'product.template',
        'Product Template',
        index=True,
        ondelete='cascade',
        oldname='product_id'
    )
    product_variant_count = fields.Integer(
        'Variant Count',
        related='product_tmpl_id.product_variant_count'
    )
