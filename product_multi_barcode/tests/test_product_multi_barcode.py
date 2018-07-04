# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests import common


# oe -Q product_multi_barcode -c iomaq -d iomaq_test


class TestProductMultiEan(common.TransactionCase):
    def setUp(self):
        super(TestProductMultiEan, self).setUp()
        self.product4 = self.env.ref(
            'product.product_product_34_product_template')
        self.product5 = self.env.ref(
            'product.product_product_35_product_template')
        self.product_barcode_obj = self.env['product.barcode']

    def test_01(self):
        """ test_01 agregar barcodes que no existen------------------------
        """
        self.product_barcode_obj.add_barcode(self.product4, 4044471900007)
        self.product_barcode_obj.add_barcode(self.product4, 4211821800007)
        self.product_barcode_obj.add_barcode(self.product4, 2112345678900)
        self.assertEqual(len(self.product4.barcode_ids), 3)

    def test_02(self):
        """ test_02 agregar barcodes que ya existen en el producto----------
        """
        self.product_barcode_obj.add_barcode(self.product4, 4044471900007)
        self.product_barcode_obj.add_barcode(self.product4, 4211821800007)
        self.product_barcode_obj.add_barcode(self.product4, 2112345678900)

        # si ya existe no lo agrega y no falla
        self.product_barcode_obj.add_barcode(self.product4, 4044471900007)
        self.assertEqual(len(self.product4.barcode_ids), 3)

    def test_03(self):
        """ test_03 agregar barcodes que ya existen en otro producto-------
        """
        self.product_barcode_obj.add_barcode(self.product4, 4044471900007)
        self.product_barcode_obj.add_barcode(self.product4, 4211821800007)
        a = self.product_barcode_obj.add_barcode(self.product4, 2112345678900)
        self.assertEqual(a, 'created')

        # debe generar execpcion de barcode duplicado
        a = self.product_barcode_obj.add_barcode(self.product5, 4044471900007)
        self.assertEqual(a, 'changed')
