# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Task2Calendar',
    'summary': """Goes from task to calendar""",
    'version': '1.0',
    'category': 'MRP',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Mackilem Van der Laan Soares <mack.vdl@gmail.com>',
                     'Danimar Ribeiro <danimaribeiro@gmail.com>'
                     ],
    'depends': [
        'project',
        'calendar',
    ],
    'data': [
        'views/trust_project.xml',
    ],
    'application': True,
}
