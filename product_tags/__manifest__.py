# Copyright 2020 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Tags",
    "summary": "Add product Tags",
    "version": "13.0.0.0.0",
    "development_status": "Production/Stable",  #  "Alpha|Beta|Production/Stable|Mature",
    "category": "Tools",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "excludes": [],
    "depends": [
        "base",
        'product'
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_view.xml",
    ],
    "demo": [
        "demo/product_tags.xml",
    ],
    "application": False,
    "installable": True,
    "preloadable": False,

}
