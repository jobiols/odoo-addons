# For copyright and license notices, see __manifest__.py file in module root


from odoo import models, api
from odoo import tools


class AccountInvoiceLineReport(models.Model):

    _inherit = "account.invoice.line.report"

    @api.model_cr
    def init(self):
        cr = self.env.cr

        tools.drop_view_if_exists(cr, 'account_invoice_line_report')
        cr.execute("""
        CREATE OR REPLACE VIEW account_invoice_line_report AS (
        SELECT
        "account_invoice_line"."id" AS "id",
        "account_invoice_line"."price_unit" AS "price_unit",
        "account_invoice_line"."discount" AS "discount",
        "account_invoice_line"."account_analytic_id" AS "account_analytic_id",
        "account_invoice_line"."price_subtotal_signed"
            AS "price_subtotal_signed",

        -- este es el fix que hacemos
        case when "account_invoice"."type" in ('in_refund','out_refund') then
                            -("account_invoice_line"."price_total")
                    else
                            "account_invoice_line"."price_total"
                    end     AS "amount_total",

        case when "account_invoice"."type" in ('in_refund','out_refund') then
                               -("account_invoice_line"."quantity")
                              else
                               "account_invoice_line"."quantity"
                              end as "quantity",
        case when "account_invoice"."type" in ('in_refund','out_refund') then
                               -("account_invoice_line"."price_subtotal")
                              else
                               "account_invoice_line"."price_subtotal"
                              end as "price_subtotal",

      -- Campos Calculados
        case when "account_invoice"."type" in ('in_refund','out_refund') then
                               -("price_unit" * "quantity")
                              else
                               ("price_unit" * "quantity")
                              end as "price_gross_subtotal",

        case when "account_invoice"."type" in ('in_refund','out_refund') then
                               -("price_unit" * "quantity" * ("discount"/100))
                              else
                               ("price_unit" * "quantity" * ("discount"/100))
                              end as "discount_amount",

        "account_invoice_line"."partner_id" AS "partner_id",--n
        "account_invoice_line"."product_id" AS  "product_id", --n
        "account_invoice"."date_due" AS "date_due",
        COALESCE("account_invoice"."document_number",
        "account_invoice"."number") AS "number",
        "account_invoice"."currency_id" AS "currency_id",
        "account_invoice"."journal_id" AS "journal_id",--n
        "account_invoice"."user_id" AS "user_id",--n
        "account_invoice"."company_id" AS "company_id",--n
        "account_invoice"."type" AS "type",
        "account_invoice"."state_id" AS "state_id",--n

        "account_invoice"."document_type_id" AS "document_type_id",
        "account_invoice"."state" AS "state",
        "account_invoice"."date" AS "date",
        "account_invoice"."date_invoice" AS "date_invoice",

--      esta es la linea que estaba mal
--      "account_invoice"."amount_total" AS "amount_total",

        "product_product"."barcode" AS "barcode",
        "product_template"."name" AS "name_template",


        "product_template"."categ_id" as "product_category_id", --n
        "res_partner"."customer" AS "customer",
        "res_partner"."supplier" AS "supplier"
        -- "account_invoice"."period_id" AS "period_id",
        -- "account_period"."fiscalyear_id" AS "fiscalyear_id"

        FROM "account_invoice_line" "account_invoice_line"
        INNER JOIN "account_invoice" "account_invoice"
        ON ("account_invoice_line"."invoice_id" = "account_invoice"."id")
        LEFT JOIN "product_product" "product_product"
        ON ("account_invoice_line"."product_id" = "product_product"."id")
        INNER JOIN "res_partner" "res_partner"
        ON ("account_invoice"."partner_id" = "res_partner"."id")
        LEFT JOIN "product_template" "product_template"
        ON ("product_product"."product_tmpl_id" = "product_template"."id")
        -- INNER JOIN "public"."account_period" "account_period"
        -- ON ("account_invoice"."period_id" = "account_period"."id")
        ORDER BY number ASC
              )""")
