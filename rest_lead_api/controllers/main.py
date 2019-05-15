# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.controllers import main
from odoo.http import route


class BaseRestPublicApiController(main.RestController):
    _root_path = '/v1/public/'
    _collection_name = 'base.rest.public.services'
    _default_auth = 'public'


class BaseRestPrivateApiController(main.RestController):
    _root_path = '/v1/private/'
    _collection_name = 'base.rest.private.services'
    _default_auth = 'api_key'
