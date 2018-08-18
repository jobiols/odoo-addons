# -*- coding: utf-8 -*-
from openerp import models, api
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    @api.constrains('main_id_number', 'main_id_category_id')
    def _check_unique_vat(self):
        for partner in self:
            code = partner.main_id_category_id.code
            number = partner.main_id_number
            if code == 'CUIT' and number:
                domain = [('main_id_number', '=', number)]
                duplicate = self.search(domain)
                if len(duplicate) > 1:
                    raise ValidationError(
                        u'El CUIT {} ya está ingresado,'.format(number))
