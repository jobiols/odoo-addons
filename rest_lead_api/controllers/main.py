# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.controllers import main
from odoo.http import route


class BaseRestDemoPublicApiController(main.RestController):
    _root_path = '/lead/v1/public/'
    _collection_name = 'base.rest.demo.public.services'
    _default_auth = 'public'


class BaseRestDemoPrivateApiController(main.RestController):
    _root_path = '/lead/v2/private/'
    _collection_name = 'base.rest.demo.private.services'
    _default_auth = 'api_key'


class BaseRestPrivateApiController(main.RestController):
    _root_path = '/lead/v1/private/'
    _collection_name = 'base.rest.private.services'
    _default_auth = 'api_key'
