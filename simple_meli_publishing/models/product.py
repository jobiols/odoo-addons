# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    meli_code = fields.Char(
        string='Meli Publishing Code'
    )

    _sql_constraints = [
        ('uniq_meli_code', 'unique(meli_code)', 'The Mercadolibre product code'
                                                ' must be unique !'),
    ]
