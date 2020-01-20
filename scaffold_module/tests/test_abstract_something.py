# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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


from odoo import api, models
from odoo.tests.common import SingleTransactionCase


class AbstractSomethingTester(models.Model):
    """ It provides a real model object to test the abstract with """
    _name = 'abstract.something.tester'
    _description = 'Abstract Something Tester'
    _inherit = 'abstract.something'


class TestAbstractSomething(SingleTransactionCase):
    @classmethod
    def _init_test_model(cls, model_cls):
        """ It builds a model from model_cls in order to test abstract models

        Args:
            model_cls: (openerp.models.BaseModel) Class of model to initialize
        Returns:
            Model instance
        """
        model_cls._build_model(cls.registry, cls.cr)
        model = cls.env[model_cls._name].with_context(todo=[])
        model._prepare_setup()
        model._setup_base(partial=False)
        model._setup_fields(partial=False)
        model._setup_complete()
        model._auto_init()
        model.init()
        model._auto_end()
        return model

    @classmethod
    def setUpClass(cls):
        super(TestAbstractSomething, cls).setUpClass()
        cls.registry.enter_test_mode()
        cls.old_cursor = cls.cr
        cls.cr = cls.registry.cursor()
        cls.env = api.Environment(cls.cr, cls.uid, {})
        cls.test_model = cls._init_test_model(AbstractSomethingTester)

    @classmethod
    def tearDownClass(cls):
        cls.registry.leave_test_mode()
        cls.registry[cls.test_model._name]._abstract = True
        cls.registry[cls.test_model._name]._auto = False
        cls.cr = cls.old_cursor
        cls.env = api.Environment(cls.cr, cls.uid, {})
        super(TestAbstractSomething, cls).tearDownClass()
