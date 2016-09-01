# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Contador de Tempo em Suporte",
    'summary': """Habilita a contagem de tempo para issues""",
    'description': """Habilita a contagem de tempo para issues""",
    'version': '8.0.1.0.0',
    'category': 'MRP',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Mackilem Van der Laan Soares <mack.vdl@gmail.com>',
                     'Danimar Ribeiro <danimaribeiro@gmail.com>',
                     'Alessandro Fernandes Martini \
                     <alessandrofmartini@gmail.com>'
                     ],
    'depends': [
        'account', 'account_analytic_analysis',
        'crm_helpdesk', 'crm_helpdesk_workflow'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_analytic.xml',
        'views/crm_helpdesk.xml',
    ],
    'application': True,
}
