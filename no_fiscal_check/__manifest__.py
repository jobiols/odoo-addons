# -*- coding: utf-8 -*-
# Copyright 2019 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Cheques no fiscales",
    "summary": "Permite poner una marca a los cheques no fiscales para diferenciarlos",
    "version": "11.0.0.0.0",
    "development_status": "Alpha",
    "category": "accounting",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'account_check',
    ],
    "data": [
        "views/account_payment_view.xml",
        "views/account_check_view.xml",
    ]
}
