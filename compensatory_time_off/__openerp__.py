# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Compensatory Time Off - Trustcode',
    'summary': """Compensatory Time Off for HR""",
    'version': '8.0',
    'category': 'Trustcode',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Danimar Ribeiro <danimaribeiro@gmail.com>',
                     'Mackilem Van der Laan Soares <mack.vdl@gmail.com>'
                     ],
    'depends': [
        'hr_attendance',
        'hr_timesheet_sheet',
        'hr_holidays',
        'resource',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_holidays.xml',
        'views/timesheet_comptime_view.xml',
        'views/hr_timesheet_sheet.xml',
        'views/hr_timesheet_overtime.xml',
    ],
    'application': True,
    'auto_install': False
}
