# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, date, timedelta
from dateutil import rrule, parser
from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from openerp.exceptions import Warning as UserError


class TimeSheetComp(models.Model):
    _inherit = 'hr_timesheet_sheet.sheet'

    @api.multi
    @api.depends('timesheet_ids')
    def _compute_overtime_to_pay(self):
        for item in self:
            total = 0.0
            for an_line in item.timesheet_ids:
                if an_line.pay_overtime:
                    total += an_line.unit_amount
            item.overtime_to_pay = total

    total_duty_hours = fields.Float(string='Total de horas')
    total_diff_hours = fields.Float('Saldo de horas do período',
                                    readonly=True, default=0.0)
    total_leave_hours = fields.Float(string="Total de horas folga")
    prev_timesheet_diff = fields.Float(compute='_overtime_diff',
                                       string="Última planilha de horários")
    calculate_diff_hours = fields.Float(compute='_overtime_diff',
                                        string="Saldo Final de horas")
    overtime_to_pay = fields.Float(string="Horas extras a pagar",
                                   compute='_compute_overtime_to_pay',
                                   store=True)

    overtime_day_ids = fields.One2many('hr.timesheet.overtime',
                                       'hr_timesheet_sheet_id',
                                       string="Dias de trabalho")

    leave_ids = fields.One2many('hr.holidays', 'timesheet_sheet_id',
                                string="Folgas")

    @api.multi
    def _get_previous_month_diff(self, employee_id, prev_timesheet_date_from):
        total_diff = 0.0
        timesheet_ids = self.search(
            [('employee_id', '=', employee_id),
             ('date_from', '<', prev_timesheet_date_from)])
        for sheet in timesheet_ids:
            total_diff += sheet.calculate_diff_hours
        return total_diff

    @api.multi
    @api.depends('prev_timesheet_diff', 'total_diff_hours')
    def _overtime_diff(self):
        for sheet in self:
            old_sheet_from = parser.parse(sheet.date_from)-timedelta(days=1)
            prev_timesheet_diff = self._get_previous_month_diff(
                sheet.employee_id.id,
                old_sheet_from.strftime('%Y-%m-%d'))
            total = sheet.total_diff_hours + prev_timesheet_diff - \
                sheet.overtime_to_pay
            sheet.calculate_diff_hours = total
            sheet.prev_timesheet_diff = prev_timesheet_diff

    def _search_leaves(self):
        leaves = self.env['hr.holidays'].search(
            [('employee_id', '=', self.employee_id.id),
             ('state', '=', 'validate'),
             ('date_from', '>=', self.date_from),
             ('date_to', '<=', self.date_to)])
        for leave in leaves:
            leave.write({
                'timesheet_sheet_id': self.id
            })

    @api.multi
    def calculate_timesheet(self):
        start_date = datetime.strptime(self.date_from, DATE_FORMAT)
        end_date = datetime.strptime(self.date_to, DATE_FORMAT)

        contract = self.env['hr.contract'].search(
            [('employee_id', '=', self.employee_id.id),
             ('date_start', '<=', date.today().strftime(DATE_FORMAT)),
             '|', ('date_end', '>=', date.today().strftime(DATE_FORMAT)),
             ('date_end', '=', None)])

        if len(contract) == 1:
            if not contract.working_hours:
                raise UserError(
                    'Atenção!', 'Defina o horário de trabalho no contrato')
            calendar = contract.working_hours

            self._search_leaves()  # Busca as folgas do funcionário

            days = rrule.rrule(
                rrule.DAILY, dtstart=start_date,
                until=(end_date).replace(hour=0, minute=0, second=0))

            total_leave_hours = 0.0
            leaves = calendar.get_leave_intervals()[0]
            for leave in self.leave_ids:
                leaves.append(
                    (datetime.strptime(leave.date_from, DATETIME_FORMAT),
                     datetime.strptime(leave.date_to, DATETIME_FORMAT))
                )
                total_leave_hours += leave.total_duty_hours_off

            dayjob_obj = self.env['hr.timesheet.overtime']
            self.overtime_day_ids.unlink()

            total_hours = 0.0
            total_worked = 0.0
            for day in days:
                string_day = day.strftime(DATE_FORMAT)

                duty_hours = calendar.get_working_hours_of_date(
                    start_dt=day, leaves=leaves)

                attendance_hours = 0.0
                attendance_day = self.period_ids.filtered(
                    lambda x: x.name == string_day)
                if attendance_day:
                    attendance_hours = attendance_day.total_attendance

                if duty_hours[0] > 0:
                    dayjob_obj.create({
                        'hr_timesheet_sheet_id': self.id,
                        'day': day,
                        'duty_hours': duty_hours[0],
                        'worked_hours': attendance_hours,
                    })
                    total_worked += attendance_hours
                    total_hours += duty_hours[0]
            self.write({
                'total_duty_hours': total_hours + total_leave_hours,
                'total_attendance': total_worked,
                'total_diff_hours': total_worked - total_hours,
                'total_leave_hours': total_leave_hours,
            })

        elif len(contract) > 1:
            raise UserError('Atenção!',
                            'Funcionário com mais de um contrato ativo')
        else:
            raise UserError('Atenção!',
                            'Funcionário sem contrato definido')
