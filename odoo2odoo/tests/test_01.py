# -*- coding: utf-8 -*-

import unittest

#    Forma de correr el test
#    -----------------------
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos no importa el nombre (por ejemplo act_test)
#   vacia y con el modulo que se va a testear instalado (por ejemplo business).
#   en -Q ponemos el repo donde vive el modulo a testear y el nombre del test
#
#   El usuario admin tiene que tener password admin, Language English, Country
#   United States.
#   -Q "repo donde esta el archivo de test" "archivo de test"
#   -c cliente
#   -d base de datos
#   -m modulo que estamos testeando
#
#   ./odooenv.py
#   -Q odoo-addons test_01.py -c bulonfer -d bulonfer_test -m odoo2odoo
#
#    si le pongo -i modulo ejecuta el yml si le pongo -u modulo no lo ejecuta.
#


class TestBackend(unittest.TestCase):
    """ Test Backend """

    def setUp(self):
        super(TestBackend, self).setUp()

    def test_new_backend(self):
        self.assertEqual(1, 1)
