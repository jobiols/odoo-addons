# -*- coding: utf-8 -*-
######################################################################################
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
######################################################################################
from openerp import models, api, fields
from openerp.exceptions import Warning


# class product_template(models.Model):
#    _inherit = 'product.template'
#    type = fields.Selection(selection_add=[('card', 'Credit Card')])


class product_product(models.Model):
    _inherit = 'product.product'

    credit_card = fields.Many2one('credit_card')
    coupon_value = fields.Float('Valor del cupon')
    plan = fields.Many2one('credit_plan')

    @api.one
    def button_calc_plan(self):
        if not self.credit_card:
            raise Warning(u'No se definió tarjeta de crédito')

        credit_plan_obj = self.env['credit_plan'].search([])

        # limpiar tabla
        for item in credit_plan_obj:
            item.unlink()

        # calcular y cargar los datos
        card_commission = self.env['card_commission'].search([('card', '=', self.credit_card.id)])
        for comm in card_commission:
            surcharge_coef = (comm.card.surcharge / 100 + 1) * comm.coefficient
            surcharge_coef = (surcharge_coef - 1)

            credit_plan_obj.create({
                'installments': comm.installment,
                'surcharge': surcharge_coef * self.coupon_value,
                'total': (1 + surcharge_coef) * self.coupon_value,
            })

    @api.onchange('plan')
    def _onchange_plan(self):
        self.lst_price = self.plan.total
