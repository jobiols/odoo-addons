# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

#   Para correr los tests
#
#   Definir un subpackage tests que será inspeccionado automáticamente por
#   modulos de test los modulos de test deben enpezar con test_ y estar
#   declarados en el __init__.py, como en cualquier package.
#
#   Hay que crear una base de datos para testing como sigue:
#   - Nombre sugerido: [nombre cliente]_test
#   - Debe ser creada con Load Demostration Data chequeado
#   - Usuario admin y password admin
#   - El modulo que se quiere testear debe estar instalado.
#
#   Arrancar el test con:
#
#   oe -Q [modulo-a-testear-] -c [cliente] -d [cliente]_test
#

from odoo.tests.common import HttpCase, TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)

        # TODO Replace this for something useful or delete this method
        self.do_something_before_all_tests()

    def tearDown(self, *args, **kwargs):
        # TODO Replace this for something useful or delete this method
        self.do_something_after_all_tests()

        return super(SomethingCase, self).tearDown(*args, **kwargs)

    def test_01_something(self):
        """TEST 01 docstring appears in test logs.
        """
        self.assertEqual(1, 1)


class UICase(HttpCase):

    post_install = True
    at_install = False

    def test_ui_web(self):
        """Test backend tests."""
        self.phantom_js(
            "/web/tests?debug=assets&module=module_name",
            "",
            login="admin",
        )

    def test_ui_website(self):
        """Test frontend tour."""
        self.phantom_js(
            url_path="/?debug=assets",
            code="odoo.__DEBUG__.services['web.Tour']"
                 ".run('test_module_name', 'test')",
            ready="odoo.__DEBUG__.services['web.Tour'].tours.test_module_name",
            login="admin")
