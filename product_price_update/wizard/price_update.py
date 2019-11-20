from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProductPriceUpdate(models.TransientModel):
    _name = 'product.price.update'

    category_filter = fields.Boolean(
        help="Determina si se va a filtrar por categorias",
        string='Filtrar por categorías',
    )
    category_ids = fields.Many2many(
        comodel_name='product.category',
        string='Indique categorías',
        help='Lista de categorías por las que se filtraran los productos'
    )
    update_type = fields.Selection(
        [('percent', 'Porcentaje'),
         ('amount', 'Monto')],
        default='percent',
        required=True,
        help='Modo en que se actualizaran los precios',
        string='Actualizar por'
    )
    update_mode = fields.Selection([
        ('sale', 'De venta'),
        ('purchase', 'De compra'),
        ('supplier_purchase', 'De compra con proveedor')],
        string="Actualizar el Precio",
        default='sale'
    )
    supplier_filter = fields.Boolean(
        help="Determina si se va a filtrar por proveedores",
        string='Filtrar por proveedores',
        domain=[]
    )
    supplier_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Indique proveedores',
        domain=[('supplier', '=', True)]
    )
    product_ids = fields.Many2many(
        comodel_name='product.template',
        string='Productos a afectar',
        help='Lista de productos que estan afectados por la modificacion'
    )
    value = fields.Float(
        "Valor",
        required=True,
        help='El valor a actualizar puede ser un porcentaje o un monto segun '
             'se selecciono en "Actualizar por", ademas puede ser positivo o '
             'negativo'
    )

    @api.onchange('update_mode')
    def onchange_update_mode(self):
        """ Si estoy en modo actualizar por proveedor requiero los proveedores
        """
        if self.update_mode == 'supplier_purchase':
            self.supplier_filter = True
        else:
            self.supplier_filter = False

    def validate_data(self):
        # Si tilde filtrar por proveedores debo poner alguno
        if self.update_mode == 'supplier_purchase' and not self.supplier_ids:
            raise UserError('Debe seleccionar al menos un proveedor.')

        # Si tilde filtrar por categorias debo poner alguna
        if self.category_filter and not self.category_ids:
            raise UserError(_('Debe seleccionar al menos una categoria.'))

    def generate_select(self):
        """ selecciona los id de product_template que vamos a actualizar
        """
        select = 'SELECT pt.id FROM product_template pt \n'

        join = 'JOIN product_supplierinfo ps \n' \
               'ON ps.product_tmpl_id = pt.id \n'

        where_list = []
        # armo la where list en una lista de clausulas where
        if self.supplier_ids:
            ids = list(map(str, self.supplier_ids.ids))
            where_list.append(
                'ps.name in (%s) ' % ','.join(ids))
        if self.category_ids:
            ids = list(map(str, self.category_ids.ids))
            where_list.append(
                'pt.categ_id in (%s) ' % ','.join(ids)
            )

        # si tengo suppliers hago el join
        if self.supplier_ids:
            select += join

        # si tengo where list agrego el WHERE
        if where_list:
            select += 'WHERE '

        # armo todas las clausulas where separandolas con AND
        select += ' AND '.join(where_list)

        return select

    def get_set_parameters(self, updated_field=False):
        if self.update_type == 'amount':
            return '{0} = {0} + {1}'.format(
                updated_field, self.value)
        else:
            return '{0} = {0} * (1 + ({1}))'.format(
                updated_field, self.value / 100)

    def _generate_sql_for_purchase(self):
        """ Genera el sql para update_mode = purchase, en este caso el campo que
            hay que modificar es standard_price que es un campo company_dependent
        """

        # obtiene los ids de los productos a actualizar
        select = self.generate_select()

        # convierte los product_template en product_product
        self.env.cr.execute(
            """
            SELECT id FROM product_product
            where product_tmpl_id in ({})
            """.format(select)
        )
        tuples = self.env.cr.fetchall()
        res_id = []

        # convierte los product_product en 'product.product,id'
        for prod_id in tuples:
            res_id.append('product.product,' + str(prod_id[0]))

        # obtiene los parametros del SET
        set = self.get_set_parameters(updated_field='value_float')

        sql = """
            UPDATE ir_property
            SET {}
            WHERE name = 'standard_price' and
                  res_id in {}
                    """.format(set, tuple(res_id))

        return sql

    def _generate_sql_for_supplier_purchase(self):
        """ Genera el sql para update_mode = supplier_purchase
            modifica el precio en el supplierinfo
        """
        # obtiene los ids de los productos a actualizar
        select = self.generate_select()

        # obtiene los parametros del SET
        set = self.get_set_parameters(updated_field='price')

        sql = """
        UPDATE product_supplierinfo
          SET {}
          WHERE id in (
                SELECT psi.id FROM product_supplierinfo psi \n
                JOIN product_template pt \n
                  ON pt.id = psi.product_tmpl_id \n
                WHERE pt.id in ({})
                )
        """.format(set, select)

        return sql

    def _generate_sql_for_sale(self):
        """ Genera el sql para update_mode = sale
        """
        select = self.generate_select()

        # obtiene los parametros del SET
        set = self.get_set_parameters(updated_field='list_price')

        sql = """
              UPDATE product_template \n
              SET {} \n
              WHERE id in ({})
              """.format(set, select)

        return sql

    def generate_sql(self):
        """ Genera el sql para modificar el precio
        """

        if self.update_mode == 'sale':
            return self._generate_sql_for_sale()
        elif self.update_mode == 'purchase':
            return self._generate_sql_for_purchase()
        else:
            return self._generate_sql_for_supplier_purchase()

    def confirm(self):
        """ Procesar la actualizacion de precios
        """
        self.validate_data()
        sql = self.generate_sql()
        self.env.cr.execute(sql)

    def check_affected(self):
        self.validate_data()
        sql = self.generate_select()
        self.env.cr.execute(sql)

        a = self.env.cr.fetchall()
        ids = []
        for b in a:
            ids.append(b[0])

        self.product_ids = self.env['product.template'].search(
            [('id', 'in', ids)])

        ret = {
            'name': 'Actualización de Precios',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.price.update',
            'target': 'new',
            'context': {
                'default_category_filter': self.category_filter,
                'default_update_type': self.update_type,
                'default_update_mode': self.update_mode,
                'default_value': self.value
            }
        }

        if self.category_filter:
            ret['context']['default_category_ids'] = self.category_ids.ids
        if self.supplier_filter:
            ret['context']['default_supplier_ids'] = self.supplier_ids.ids
        if self.product_ids:
            ret['context']['default_product_ids'] = self.product_ids.ids

        return ret
