# For copyright and license notices, see __manifest__.py file in module root

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    packages = fields.Integer(
        'Paquete',
        help='Cantidad de elementos en el bulto'
    )
