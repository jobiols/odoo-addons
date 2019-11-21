# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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
#   Debe tener usuario admin y password admin y demo data
#
#   Arrancar el test con:
#
#   oe -Q gapp_logistic_connector -c botella -d botella_test
#


from openerp.tests.common import HttpCase, TransactionCase


class SomethingCase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)

        # TODO Replace this for something useful or delete this method
        self.do_something_before_all_tests()

    def tearDown(self, *args, **kwargs):
        # TODO Replace this for something useful or delete this method
        self.do_something_after_all_tests()

        return super(SomethingCase, self).tearDown(*args, **kwargs)

    def test_something(self):
        """First line of docstring appears in test logs.

        Other lines do not.

        Any method starting with ``test_`` will be tested.
        """
        pass


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
