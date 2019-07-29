# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class SaleOrder_line(models.Model):
    _inherit = 'sale.order.line'

    unit_type = fields.Selection([
        ('unit', 'Unidad'),
        ('pair', 'Par')],
        string='Tipo de unidad'
    )
