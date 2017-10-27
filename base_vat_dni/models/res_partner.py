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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.constrains('responsability_id')
    def _check_responsability(self):
        for partner in self:
            # chequear Si es responsable inscripto o monotributo requiere CUIT
            if partner.responsability_id.code == '1' or \
               partner.responsability_id.code == '6':       # responsable inscripto o monotributo
                if partner.document_type_id.name != 'CUIT':
                    raise ValidationError(u'Para ingresar un cliente "{}" Se requiere CUIT'.
                                          format(partner.responsability_id.name))

    @api.multi
    @api.constrains('document_number')
    def _check_document_type(self):
        for partner in self:
            # verifica que el DNI sea numerico
            if partner.document_type_id.name == 'DNI':
                try:
                    int(partner.document_number) + 1
                except:
                    raise ValidationError(u'El DNI debe contener solo numeros')

    @api.multi
    @api.constrains('document_number')
    def _check_unique_dni(self):
        for partner in self:
            if partner.document_type_id.name == 'DNI':
                recordset = self.search([('document_number', '=', partner.document_number)])
                if len(recordset) > 1:
                    raise ValidationError('El DNI {} ya está ingresado'.format(partner.document_number))

