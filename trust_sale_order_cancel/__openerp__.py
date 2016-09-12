# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Trust Sale Order Cancel",
    'summary': """Cria um botão para cancelar parcialmente produtos dos \
pedidos""",
    'version': '8.0.1.0',
    'category': 'MRP',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Mackilem Van der Laan Soares <mack.vdl@gmail.com>',
                     'Danimar Ribeiro <danimaribeiro@gmail.com>',
                     'Alessandro Fernandes Martini \
<alessandrofmartini@gmail.com>'
                     'Jenifer Rocha <@.com>',
                     'Marcos Abreu <@.com>'
                     ],
    'depends': [
        'sale', 'procurement',
    ],
    'data': [
        'views/trust_sale_order_cancel.xml',
        'views/stock_picking.xml',
        'wizard/sale_order_cancel_action.xml'
    ],
    'application': True,
}
