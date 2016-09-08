# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CRM Helpdesk Improvements',
    'summary': """Adiciona um workflow dinâmico ao CRM Helpdesk.""",
    'version': '8.0.1.0.0',
    'category': 'CRM',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Alessandro Fernandes Martini <alessandrofmartini@gmail.com>'
    ],
    'depends': [
        'product_equipment', 'crm',
    ],
    'data': [
        'data/crm_helpdesk_data.xml',
        'security/ir.model.access.csv',
        'views/crm_helpdesk.xml',
    ],
}
