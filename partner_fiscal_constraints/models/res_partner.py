# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

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

    @api.multi
    @api.constrains('vat')
    def _check_unique_vat(self):
        for partner in self:
            if partner.document_type_id.name == 'CUIT':
                recordset = self.search([('vat', '=', partner.vat)])
                if len(recordset) > 1:
                    raise ValidationError('El CUIT {}-{}-{} ya está ingresado'.format(
                            partner.vat[2:4], partner.vat[4:12], partner.vat[12:13]))

    @api.multi
    @api.constraints('responsability_id')
    def _check_address_exist(self):
        for partner in self:
            if not partner.street and partner.responsability_id.code == '1':
                raise ValidationError('Un responsable inscripto debe tener direccion')
