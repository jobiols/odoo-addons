.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

Ticket CITI Fix
===============

Agrega un tipo de punto de venta Controlador Fiscal
Si el punto de venta es Controlador Fiscal en el citi exporta ceros en lugar
de la fecha de vencimiento

Por otro lado ese fix sobreescribe una funcion **get_REGINFO_CV_CBTE** de la
clase **account_vat_ledger** lo cual lo hace peligroso porque enmascara futuros
cambios en el codigo base de adhoc.
