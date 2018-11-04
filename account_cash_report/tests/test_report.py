# -*- coding: utf-8 -*-
# For copyright and license notices, see __manifest__.py file in module root

#    Forma de correr el test
#    -----------------------
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos no importa el nombre pero se sugiere
#   [nombre cliente]_test_[nombre modulo] que debe estar vacia pero con el
#   modulo que se quiere testear instalado.
#
#   Debe tener usuario admin y password admin
#
#   Arrancar el test con:
#
#   oe -Q account_cash_report -c iomaq -d iomaq_test_account_cash_report
#
from openerp.tests import common


class TestXxxxx(common.TransactionCase):
    """ Cada metodo de test corre en su propia transacción y se hace rollback
        despues de cada uno.
    """
    def setUp(self):
        super(TestXxxxx, self).setUp()

    def test_01_(self):
        self.assertEqual(1, 1)
