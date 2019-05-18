# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, tools, _
from odoo.tools import config
from odoo.tools import consteq
from odoo.exceptions import ValidationError, AccessError


class AuthApiKey(models.TransientModel):
    _name = "auth.api.key"
    _description = "API Key Retriever"

    @api.model
    @tools.ormcache("api_key")
    def _retrieve_uid_from_api_key(self, api_key):
        if not self.env.user.has_group("base.group_system"):
            raise AccessError(_("User is not allowed"))

        if not consteq(api_key, config.get('rest_api_key')):
            return False

        login_name = config.get('rest_api_user')
        uid = self.env["res.users"].search([("login", "=", login_name)]).id

        if not uid:
            raise ValidationError(
                _("No user found with login %s") % login_name)

        return uid
