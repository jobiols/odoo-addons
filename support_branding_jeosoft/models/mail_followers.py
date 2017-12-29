# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp.osv import osv


class MailNotification(osv.Model):
    _inherit = 'mail.notification'

    def get_signature_footer(self, cr, uid, user_id, res_model=None,
                             res_id=None, context=None, user_signature=True):
        web = self.pool.get("ir.config_parameter").get_param(
            cr, uid, "support_branding.company_url",
            default=None, context=context)

        ret = super(MailNotification, self).get_signature_footer(
            cr, uid, user_id, res_model, res_id, context, user_signature)

        if web:
            ret = ret.replace('https://www.odoo.com', web)

        return ret
