# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


#   Agrega un campo en el tax para poner en la factura, esto permite que no
#   aparezcan ciertos impuestos en cada linea tipo percepciones de ingresos
#   brutos.
#   Ademas permite acortar la descripción en lugar IVA 21% ponemos 21%


class account_tax(models.Model):
    _inherit = 'account.tax'

    short_description = fields.Char()
