# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    meshops_code = fields.Boolean(
        string='Published on Mercadoshops'
    )
