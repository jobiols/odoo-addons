# -*- coding: utf-8 -*-

from openerp import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class pos_session(models.Model):
    _inherit = 'pos.session'

    is_fiscal = fields.Boolean(
        related='config_id.journal_id.is_fiscal'
    )

    @api.multi
    def test_uno(self):
        my_pos_config = self.config_id.journal_id.diario_fiscal
        if self.config_id.journal_id.is_fiscal and my_pos_config.id:
            #Si es fiscal
            my_session = self.env['pos.session'].search(
                [('config_id', '=', my_pos_config.id),
                 ('state', '=', 'opened')])

            for ped in self.order_ids:
                if not ped.invoice_id.id:
                    #Si el pedido no tiene factura.
                    ped.session_id = my_session.id
                    for st in ped.statement_ids:
                        statement = my_session.statement_ids.filtered(
                            lambda a: a.journal_id.id == st.statement_id.journal_id.id)
                        st.statement_id = statement[0].id

    def wkf_action_close(self):
        self.test_uno()
        return super(pos_session,self).wkf_action_close()
