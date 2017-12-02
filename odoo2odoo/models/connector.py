# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models, api
from openerp.addons.connector.connector import Environment


class OdooBaseBindings(models.AbstractModel):
    _name = 'odoo_base.binding'
    _inherit = 'external.binding'
    _description = 'Odoo Base Bindings (Abstract)'

    # 'odoo_id': openerp-side id must be declared in concrete model
    backend_id = fields.Many2one(
        comodel_name='odoo_base.backend',
        string='Odoo Base Backend',
        required=True,
        ondelete='restrict'
    )
    odoo_base_id = fields.Integer(
        string='ID in the odoo base',
        select=True
    )


def get_environment(session, model_name, backend_id):
    """ Create an environment to work with. """
    
    backend_record = session.env['odoo_base.backend'].browse(backend_id)
    env = Environment(backend_record, session, model_name)
    lang = backend_record.default_lang_id
    lang_code = lang.code if lang else 'en_US'
    if lang_code == session.context.get('lang'):
        return env
    else:
        with env.session.change_context(lang=lang_code):
            return env

