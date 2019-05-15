# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import jsondiff

from .common import CommonCase, get_canonical_json


class TestOpenAPI(CommonCase):
    def _fix_server_url(self, openapi_def):
        # The server url depends of base_url. base_url depends of the odoo
        # config
        url = openapi_def['servers'][0]['url']
        url.replace('http://localhost:8069', self.base_url)
        openapi_def['servers'][0]['url'] = url

    def test_lead_api(self):
        lead_service = self.private_services_env.component(usage="lead")
        openapi_def = lead_service.to_openapi()
        canonical_def = get_canonical_json("lead_api.json")
        self._fix_server_url(canonical_def)
        self.assertFalse(jsondiff.diff(openapi_def, canonical_def))
