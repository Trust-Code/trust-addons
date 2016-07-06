# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class HrTimesheetOvertime(models.Model):
    _name = 'hr.timesheet.overtime'

    @api.multi
    @api.depends('duty_hours', 'worked_hours')
    def _calculate_balance_hours(self):
        for item in self:
            item.balance_hours = item.worked_hours - item.duty_hours

    day = fields.Date(string="Dia")
    duty_hours = fields.Float(string="Horas diárias")
    worked_hours = fields.Float(string="Horas Trabalhadas")

    balance_hours = fields.Float(string="Saldo de horas",
                                 compute='_calculate_balance_hours')

    hr_timesheet_sheet_id = fields.Many2one('hr_timesheet_sheet.sheet',
                                            string="Planilha de horas")
