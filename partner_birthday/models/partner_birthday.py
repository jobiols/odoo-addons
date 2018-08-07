# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
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
# -----------------------------------------------------------------------------------
from datetime import datetime, date

from openerp import models, fields, api


class res_partner(models.Model):
    _inherit = "res.partner"

    @api.one
    @api.depends('date')
    def _get_birthday(self):
        if self.date:
            dob = datetime.strptime(self.date, '%Y-%m-%d').date()
            month = dob.month
            day = dob.day
            self.birthday = datetime(year=date.today().year,
                                     month=month,
                                     day=day).strftime('%d/%m/%Y')

    @api.one
    @api.depends('date')
    def _get_birthday_month(self):
        if self.date:
            try:
                dob = datetime.strptime(self.date, '%Y-%m-%d').date()
                self.birthday_month = dob.strftime('%b').capitalize()
            except:
                self.birthday_month = 'Error'

    @api.one
    def _get_age(self):
        if self.date:
            try:
                today = date.today()
                dob = datetime.strptime(self.date, '%Y-%m-%d').date()
                years = today.year - dob.year
                if today.month < dob.month or (
                                today.month == dob.month and today.day < dob.day):
                    years -= 1
                self.age = years
            except:
                self.age = 1

    birthday = fields.Char(compute='_get_birthday', string=u'Cumpleaños', store=True)
    birthday_month = fields.Char(compute='_get_birthday_month', string='Mes', store=True)
    age = fields.Integer(compute='_get_age', string='Edad')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
