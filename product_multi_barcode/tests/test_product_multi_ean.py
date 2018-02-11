# -*- coding: utf-8 -*-
# © 2016 Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


# oe -Q product_multi_ean -c iomaq -d iomaq_test


class TestProductMultiEan(common.TransactionCase):
    def setUp(self):
        super(TestProductMultiEan, self).setUp()
        self.product4 = self.env.ref('product.product_product_4')
        self.product5 = self.env.ref('product.product_product_5')

    def test_01(self):
        """ test_01 agregar barcodes que no existen------------------------
        """
        self.product4.add_barcodes(
            ['4044471900007', '4211821800007', '2112345678900'])
        self.assertEqual(len(self.product4.ean13_ids), 3)

    def test_02(self):
        """ test_02 agregar barcodes que ya existen en el producto----------
        """
        self.product4.add_barcodes(
            ['4044471900007', '4211821800007', '2112345678900'])

        # si ya existe no lo agrega y no falla
        self.product4.add_barcodes(['4044471900007'])
        self.assertEqual(len(self.product4.ean13_ids), 3)

    def test_03(self):
        """ test_03 agregar barcodes que ya existen en otro producto-------
        """
        self.product4.add_barcodes(
            ['4044471900007', '4211821800007', '2112345678900'])

        # debe generar execpcion de barcode duplicado
        with self.assertRaises(Exception):
            self.product5.add_barcodes(['4044471900007'])
