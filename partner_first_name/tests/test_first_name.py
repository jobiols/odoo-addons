# -*- coding: utf-8 -*-
#####################################################################################
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
#####################################################################################
from openerp.tests.common import TransactionCase


class Test(TransactionCase):
    def setUp(self):
        super(Test, self).setUp()

        print 'test_first_name----------------------------------------------'
        # cargar un cliente
        self.partner = self.env['res.partner'].create({'name': 'juan perez'})

    def test_name(self):
        self.assertEquals(self.partner.first_name, 'juan1',
                          u'Falla el modulo, el nombre debe ser juan')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: