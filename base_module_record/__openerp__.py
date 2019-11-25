# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
{
    'name': 'Record and Create Modules',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'description': """
This module allows you to create a new module without any development.
======================================================================

It records all operations on objects during the recording session and
produce a .ZIP module. So you can create your own module directly from
the OpenERP client.

This version works for creating and updating existing records. It recomputes
dependencies and links for all types of widgets (many2one, many2many, ...).
It also support workflows and demo/update data.

This should help you to easily create reusable and publishable modules
for custom configurations and demo/testing data.

How to use it:

Run Administration/Customization/Module Creation/Export Customizations As a
Module wizard.

Select datetime criteria of recording and objects to be recorded and Record
module.

    """,
    'author': 'OpenERP SA, Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.openerp.com, http://www.serpentcs.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/base_module_record_object_view.xml',
        'wizard/base_module_record_data_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'images': ['static/description/record_banner.png'],
}