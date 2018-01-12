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
from openerp import fields, models, api, _


class afip_point_of_sale(models.Model):
    _inherit = 'afip.point_of_sale'

    type = fields.Selection(
        selection_add=[('fiscal_controller', 'Controlador Fiscal')]
    )

    @api.one
    @api.depends('type', 'sufix', 'prefix', 'number')
    def get_name(self):
        # TODO mejorar esto y que tome el lable traducido del selection
        if self.type == 'manual':
            name = 'Manual'
        elif self.type == 'preprinted':
            name = 'Preimpresa'
        elif self.type == 'online':
            name = 'Online'
        elif self.type == 'electronic':
            name = 'Electronica'
        elif self.type == 'fiscal_controller':
            name = 'Controlador Fiscal'
        if self.prefix:
            name = '%s %s' % (self.prefix, name)
        if self.sufix:
            name = '%s %s' % (name, self.sufix)
        name = '%04d - %s' % (self.number, name)
        self.name = name

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
