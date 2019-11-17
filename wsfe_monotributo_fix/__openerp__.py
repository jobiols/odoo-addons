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
{
    "name": "Patch for wsfe para monotributo",
    "version": "8.0.0.1.0",
    "author": "jeo Software",
    'website': 'http://www.jeosoft.com.ar',
    "depends": ['l10n_ar_afipws_fe'],
    "category": "Generic Modules",
    "description": """
Fix para emitir facturas electrónicas como monotributista
=========================================================
Este módulo corrige un bug que impide generar facturas electrónicas
si se configura como monotributo.

No debe instalarse si la responsabilidad de la empresa es Responsable Inscripto

Sobreescribe la función do_pyafipws_request_cae del módulo l10n_ar_afipws_fe que
es muuuuy grande asi que cualquier actualización de esa función posterior a la
fecha de este módulo se perderá.

El código modificado está marcado con ## wsfe_monotributo_fix

""",
    "demo_xml": [],
    "data": [ ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [ ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
