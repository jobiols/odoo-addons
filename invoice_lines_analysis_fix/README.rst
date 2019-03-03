.. |company| replace:: jeo Soft

.. |company_logo| image:: https://gist.github.com/jobiols/74e6d9b7c6291f00ef50dba8e68123a6/raw/fa43efd45f08a2455dd91db94c4a58fd5bd3d660/logo-jeo-150x68.jpg
   :alt: jeo Soft
   :target: https://www.jeosoft.com.ar

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==========================
Invoice Lines Analysis FIX
==========================

This module fixes a bug in invoice lines analysis

BUG:
In the pivot table, the measure Price Total (Total Factura) summarizes the
whole invoice for each invoice line giving an erroneous value.

Fixed:
In the pivot table, the measure Price Total (Total Factura) summarizes the
invoice line total price for each invoice line giving the right value.


Installation
============

To install this module, you need to:

#. Just intall it.

Configuration
=============

To configure this module, you need to:

#. No configuration needed

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/jobiols/[reponame]/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

Maintainer
----------

|company_logo|

This module is maintained by |company|.

To contribute to this module, please
contact Jorge Obiols <jorge.obiols@gmail.com>
