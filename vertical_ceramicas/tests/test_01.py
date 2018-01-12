# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
# Forma de correr el test
# Crear un cliente test, una bd test_pricelist, el modulo
# test_pricelist_import cargado y un usuario admin / admin
# OJO cambiarle el path donde está el archivo a importar, esta en
# lugares distintos para travis o local
# ./odooenv.py -Q reves test_01.py -c reves -d reves_travis -m reves_default
from openerp.tests.common import SingleTransactionCase


class TestCeramicas(SingleTransactionCase):
    def setUp(self):
        super(TestCeramicas, self).setUp()

    def test_01_1(self):
        self.assertEqual(1, 1)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
