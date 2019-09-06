from odoo import fields, models, api
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
            raise UserError('Debe seleccionar al menos una categoria.')

    def generate_select(self):
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

        ##################################################
        # Armando el select
        ##################################################

        # si tengo suppliers hago el join
        if self.supplier_ids:
            select += join

        # si tengo where list agrego el WHERE
        if where_list:
            select += 'WHERE '

        # armo todas las clausulas where separandolas con AND
        select += ' AND '.join(where_list)

        return select

    def generate_sql(self):
        select = self.generate_select()

        ##################################################
        # Armando el update
        ##################################################

        if self.update_mode == 'sale':
            field = 'list_price'
        if self.update_mode == 'purchase':
            field = 'standard_price'
        if self.update_mode == 'supplier_purchase':
            field = 'price'

        if self.update_type == 'amount':
            set = 'SET {0} = {0} + {1}'.format(field, self.value)

        if self.update_type == 'percent':
            set = 'SET {0} = {0} *(1 + ({1}))'.format(field, self.value / 100)

        sql = 'UPDATE product_template \n' \
              '{} \n' \
              'WHERE id in ({})'.format(set, select)
        return sql

    def confirm(self):
        """ Procesar la actualizacion de precios
        """
        self.validate_data()

        sql = self.generate_sql()
        print(sql)
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
