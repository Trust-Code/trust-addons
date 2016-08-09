# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Equipment',
    'summary': """Adiciona alguns campos na visão de \
    produtos relacionados a TI.
    Adiciona um workflow dinâmico ao CRM Helpdesk.""",
    'version': '8.0.1.0.0',
    'category': 'Website',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Alessandro Fernandes Martini <alessandrofmartini@gmail.com>'
    ],
    'depends': [
        'product', 'account', 'crm',
    ],
    'data': [
        'views/product_template.xml',
        'views/sale_contact_template.xml',
        'views/crm_view.xml',
        'views/crm_helpdesk.xml',
    ],
}
