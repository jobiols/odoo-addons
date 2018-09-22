# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _


class Project(models.Model):
    _inherit = "project.project"

    purchase_count = fields.Integer(
        compute='_compute_purchase_count'
    )
    sales_count = fields.Integer(
        compute='_compute_sales_count'
    )
    work = fields.Char(

    )
    obs = fields.Char(

    )
    status = fields.Selection(
        [
            ('not_started', 'Not Started'),
            ('on_progress', 'On progress'),
            ('delivered', 'Delivered')
        ]
    )
    type = fields.Char(

    )
    total_sales = fields.Float(
        compute='_compute_total_sales'
    )

    @api.multi
    def _compute_total_sales(self):
        for proj in self:
            analytic = proj.analytic_account_id
            domain = [('order_id.analytic_account_id.id', '=', analytic.id)]
            proj_sales = self.env['sale.order.line'].search(domain)
            total = 0.0
            for sale in proj_sales:
                total += sale.price_subtotal
            proj.total_sales = total

    @api.multi
    def _compute_purchase_count(self):
        for proj in self:
            analytic = proj.analytic_account_id
            _obj = self.env['purchase.order.line']
            domain = [('order_id.analytic_account_id.id', '=', analytic.id)]
            proj.purchase_count = _obj.search_count(domain)

    def _compute_sales_count(self):
        for proj in self:
            analytic = proj.analytic_account_id
            _obj = self.env['sale.order.line']
            domain = [('order_id.analytic_account_id.id', '=', analytic.id)]
            proj.sales_count = _obj.search_count(domain)

    @api.multi
    def action_view_sales(self):
        self.ensure_one()
        action = self.env.ref('sale.action_product_sale_list')
        analytic = self.analytic_account_id
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'res_model': action.res_model,
            'domain': [('order_id.analytic_account_id.id', '=', analytic.id)],
        }

    @api.multi
    def action_view_purchases(self):
        self.ensure_one()
        analytic = self.analytic_account_id
        return {
            'name': _('Purchase Order Lines'),
            'help': False,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'target': 'current',
            'res_model': 'purchase.order.line',
            'domain': [('order_id.analytic_account_id.id', '=', analytic.id)],
        }
