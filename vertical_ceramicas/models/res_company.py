# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class res_company(models.Model):
    _inherit = "res.company"

    report_send_comment = fields.Text(
            'Comentario para envios a domicilio se muestra en los remitos',
            required=False
    )

    store_addresses = fields.Text(
            'Direcciones de las sucursales',
            required=False
    )
