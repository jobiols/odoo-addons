# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component
from odoo.addons.base_rest.components.service import skip_secure_response
from odoo.addons.base_rest.components.service import to_int, to_bool


class TeamService(Component):
    _inherit = 'base.rest.service'
    _name = 'team.service'
    _usage = 'team'
    _collection = 'base.rest.private.services'
    _description = """
        Team Services are Autenticated by api_key.
    """

    def search(self, name):
        """
        Get all teams that use leads, name not used
        """
        teams = self.env['crm.team'].search([('use_leads', '=', True)])
        rows = []
        res = {
            'count': len(teams),
            'rows': rows
        }
        for team in teams:
            rows.append(self._to_json(team))
        return res

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env['crm.team'].browse(_id)

    def _prepare_params(self, params):
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
            'name': {'type': 'string', 'nullable': False, 'required': True},
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
        }
        return res

    """
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
    """

    def _to_json(self, team):
        res = {
            'id': team.id,
            'name': team.name,
        }
        return res
