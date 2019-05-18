# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Rest Lead API',
    'summary': """
        REST API for the generation of Leads""",
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'development_status': 'Beta',
    'license': 'AGPL-3',
    'author': 'NTSystemWork',
    "maintainers": ['lmignon'],
    'website': 'https://ntsystemwork.com',
    'depends': [
        'base_rest',
        'component',
        'auth_api_ley',
        'crm'
    ],
    'data': [
    ],
    'demo': [
    ],
    'external_dependencies': {
        'python': [
            'jsondiff'
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
