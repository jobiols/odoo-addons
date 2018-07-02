# -*- coding: utf-8 -*-
from openerp import models, api
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.one
    @api.constrains('main_id_number', 'main_id_category_id')
    def _check_unique_vat(self):
        if self.main_id_category_id.code == 'CUIT':
            if self.main_id_number:
                domain = [('main_id_number', '=', self.main_id_number)]
                recordset = self.search(domain)
                if len(recordset) > 1:
                    raise ValidationError(
                        u'El CUIT {} ya está ingresado'.format(
                            self.main_id_number))
