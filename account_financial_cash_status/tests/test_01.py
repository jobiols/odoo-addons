# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
# Forma de correr el test
# Crear un cliente test, una bd test_cash, el modulo account_financial_cash_status instalado y un usuario admin / admin

# ./odooenv.py -Q odoo-addons test_01.py -c test -d test_cash -m account_financial_cash_status
# si se quiere usar wdb agregar --debug

from openerp.tests.common import SingleTransactionCase
from openerp.tools import test_reports
from openerp import api, fields, models, _


class TestReves(SingleTransactionCase):
    def setUp(self):
        super(TestReves, self).setUp()


    def test_01_1(self):
        ctx = {'landscape': True}

        print 'testing report ================================================================================='

        #import wdb;wdb.set_trace()
        acc_chart = self.registry("ir.model.data").get_object_reference(
                self.env.cr,
                self.env.uid, "account", "chart0")

        data_dict = {'chart_account_id': acc_chart}

#        test_reports.try_report_action(
#                self.env.cr,
#                self.env.uid,
#                'action_account_cash_menu',
#                wiz_data=data_dict,
#                context=ctx,
#                our_module='account_financial_cash_status')

    #test_reports.try_report_action(cr, uid,
        # 'action_account_general_ledger_menu',
        # wiz_data=data_dict,
        # context=ctx,
        # our_module='account')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
