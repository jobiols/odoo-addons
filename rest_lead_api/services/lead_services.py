# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.addons.base_rest.components.service import to_int, to_bool


class LeadService(Component):
    _inherit = 'base.rest.service'
    _name = 'lead.service'
    _usage = 'lead'
    _collection = 'base.rest.private.services'
    _description = """
        Lead Services
        Access to the lead services is only allowed to authenticated users.
    """

    @skip_secure_response
    def get(self, _id):
        """
        Get lead's informations
        """
        return self._to_json(self._get(_id))

    def search(self, name):
        """
        Searh lead by name
        """
        leads = self.env['crm.leads'].name_search(name)
        leads = self.env['crm.leads'].browse([i[0] for i in leads])
        rows = []
        res = {
            'count': len(leads),
            'rows': rows
        }
        for lead in leads:
            rows.append(self._to_json(lead))
        return res

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new lead
        """
        lead = self.env['crm.lead'].create(
            self._prepare_params(params))
        return self._to_json(lead)

    def update(self, _id, **params):
        """
        Update lead informations
        """
        lead = self._get(_id)
        lead.write(self._prepare_params(params))
        return self._to_json(lead)

    """
    def archive(self, _id, **params):
        " ""
        Archive the given partner. This method is an empty method, IOW it
        don't update the partner. This method is part of the demo data to
        illustrate that historically it's not mandatory to defined a schema
        describing the content of the response returned by a method.
        This kind of definition is DEPRECATED and will no more supported in
        the future.
        :param _id:
        :param params:
        :return:
        " ""
        return {'response': 'Method archive called with id %s' % _id}
    """
    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env['crm.lead'].browse(_id)

    def _prepare_params(self, params):
        for key in ['country', 'state']:
            if key in params:
                val = params.pop(key)
                if val.get('id'):
                    params["%s_id" % key] = val['id']
        return params

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({
            'id': {'type': 'integer', 'required': True, 'empty': False},
        })
        return res

    def _validator_search(self):
        return {
            'name': {
                'type': 'string',
                'nullable': False,
                'required': True,
                },
            }

    def _validator_return_search(self):
        return {
            'count': {'type': 'integer', 'required': True},
            'rows': {
                'type': 'list',
                'required': True,
                'schema': {
                    'type': 'dict',
                    'schema': self._validator_return_get()
                }
            }
        }

    def _validator_create(self):
        res = {
            'name': {'type': 'string', 'required': True, 'empty': False},
            'street': {'type': 'string', 'required': False, 'empty': True},
            'mobile': {'type': 'string', 'required': False, 'empty': True},
            'contact_name': {'type': 'string', 'required': False, 'empty': True},
            'email_from': {'type': 'string', 'required': False, 'empty': True},
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if 'required' in res[key]:
                del res[key]['required']
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, lead):

        res = {
            'id': lead.id,
            'name': lead.name,
            'street': lead.street or '',
            'mobile': lead.mobile or '',
            'contact_name': lead.contact_name or '',
            'email_from': lead.email_from or '',
        }
        return res
