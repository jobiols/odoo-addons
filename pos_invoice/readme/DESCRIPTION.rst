Este modulo intercepta el reporte point_of_sale.report_invoice que es la
factura standard de odoo y la cambia por l10n_ar_aeroo_einvoice.aeroo_report_ar_einvoice
que es la factura electronica AFIP.

De esa forma al facturar desde el POS baja la factura electronica en lugar de
bajar la factura original odoo.

NOTA: para ubicar la factura que tiene que reportar busca el ultimo id de factura
que se hizo con lo cual si hay varias instancias POS facturando al mismo tiempo
se puede dar un race condition que no garantiza que se imprima la factura correcta.