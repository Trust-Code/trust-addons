# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Importação de clientes',
    'summary': """Importador de clientes especifico""",
    'version': '8.0.1.0.0',
    'category': 'sale',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>'
    ],
    'depends': [
        'crm',
    ],
    'data': [
        'wizard/base_import_partner.xml',
    ],
}
