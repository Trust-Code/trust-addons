# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Helpdesk',
    'summary': "Cria um botão que transfere do helpdesk para a cotação.",
    'version': '8.0.1.0.0',
    'category': 'Website',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Alessandro Fernandes Martini <alessandrofmartini@gmail.com>'
    ],
    'depends': ['crm_helpdesk', 'sale'],
    'data': [
        'views/crm_helpdesk_sale_order_link_view.xml',
        'views/crm_helpdesk_sale_order.xml',
    ],
}
