# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    timesheet_sheet_id = fields.Many2one('hr_timesheet_sheet.sheet',
                                         string="Planilha de horas")
