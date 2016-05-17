# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project My Task',
    'summary': """Add My Task Button to Kanban View""",
    'version': '1.0',
    'category': 'project',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>'
    ],
    'depends': [
        'project',
    ],
    'data': [
        'views/task_kanban_view.xml',
    ],
    'application': True,
}
