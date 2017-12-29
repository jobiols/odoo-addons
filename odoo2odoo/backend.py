# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import openerp.addons.connector.backend as backend

odoo_base = backend.Backend('odoo_base')
odoo90 = backend.Backend(parent=odoo_base, version='9.0')
