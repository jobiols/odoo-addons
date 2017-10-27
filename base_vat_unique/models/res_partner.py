# -*- encoding: utf-8 -*-
##################################################################################
#    Copyright (C) 2016  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from openerp import models, api
from openerp.exceptions import ValidationError


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.constrains('vat')
    def _check_unique_vat(self):
        for partner in self:
            if partner.document_type_id.name == 'CUIT':
                recordset = self.search([('vat', '=', partner.vat)])
                if len(recordset) > 1:
                    raise ValidationError('El CUIT {}-{}-{} ya está ingresado'.format(
                            partner.vat[2:4], partner.vat[4:12], partner.vat[12:13]))
