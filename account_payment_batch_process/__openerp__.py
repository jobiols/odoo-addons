# Copyright 2019 Open Source Integrators
# <https://www.opensourceintegrators.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Proceso de pago por lotes",
    "summary": "Permite pagar facturas en lote determinando si se paga el "
               "total o solo una parte",
    "version": "9.0.0.0.0",
    "license": "AGPL-3",
    "author": "Jeo Software, Open Source Integrators, Odoo Community Association (OCA)",
    "category": "Generic Modules/Payment",
    "website": "https://github.com/jobiols/odoo-addons",
    "depends": [
        "account_payment_group"
    ],
    "data": [
        "wizard/invoice_batch_process_view.xml",
        "views/invoice_view.xml"
    ],
    "application": False,
}
