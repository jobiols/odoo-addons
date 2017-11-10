# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, api
from openerp.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.constrains('responsability_id', 'document_type_id', 'street')
    def _check_responsability(self):
        for partner in self:
            # chequear Si es responsable inscripto o monotributo requiere CUIT y direccion
            if partner.responsability_id.code == '1' or \
               partner.responsability_id.code == '6':       # responsable inscripto o monotributo
                if partner.document_type_id.name != 'CUIT':
                    raise ValidationError(u'Para ingresar un cliente "{}" Se requiere CUIT'.
                                          format(partner.responsability_id.name))
                if not partner.street:
                    raise ValidationError(u'Para ingresar un cliente "{}" se requiere direccion'.
                                          format(partner.responsability_id.name))

            if partner.responsability_id.code == '5':       # consumidor final
                if partner.document_type_id.code == 'Sigd':
                    # Este es el consumidor final anonimo para menos de $1000
                    return True

                if partner.document_type_id.name != 'DNI':
                    raise ValidationError(u'Para ingresar un cliente "{}" al que le vamos \n'
                                          u'a facturar mas de $1000 Se requiere DNI'.
                                          format(partner.responsability_id.name))
                if not partner.street:
                    raise ValidationError(u'Para ingresar un cliente "{}" al que le vamos \n'
                                          u'a facturar mas de $1000 se requiere direccion'.
                                          format(partner.responsability_id.name))


    @api.multi
    @api.constrains('document_type_id','document_number')
    def _check_unique_dni(self):
        for partner in self:
            if partner.document_type_id.name == 'DNI':
                recordset = self.search([('document_number', '=', partner.document_number)])
                if len(recordset) > 1:
                    raise ValidationError(u'El DNI {} ya está ingresado'.format(partner.document_number))

    @api.multi
    @api.constrains('vat','document_type_id')
    def _check_unique_vat(self):
        for partner in self:
            if partner.document_type_id.name == 'CUIT':
                recordset = self.search([('vat', '=', partner.vat)])
                if len(recordset) > 1:
                    raise ValidationError(u'El CUIT {}-{}-{} ya está ingresado'.format(
                            partner.vat[2:4], partner.vat[4:12], partner.vat[12:13]))


    @api.multi
    @api.constrains('document_number')
    def _check_document_type(self):
        for partner in self:
            # verifica que el DNI sea numerico
            if partner.document_type_id.name == 'DNI':
                if partner.document_number != re.sub("[^0-9]", "", partner.document_number):
                    raise ValidationError(u'El DNI "{}" debe contener solo numeros'.
                                          format(partner.document_number))
