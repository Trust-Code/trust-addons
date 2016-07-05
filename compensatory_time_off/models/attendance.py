# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

import math
from openerp import api,fields,models,tools
from datetime import datetime

class TimeSheetComp(models.Model):
    _inherit = 'hr_timesheet_sheet.sheet'

    @api.multi
    def _duty_hours(self, name, args, context=None):
        res = {}
        if not context:
            context = {}
        for sheet in self.browse(ids, context=context or {}):
            res.setdefault(sheet.id, {
                'total_duty_hours': 0.0,
            })
            if sheet.state == 'done':
                res[sheet.id]['total_duty_hours'] = sheet.total_duty_hours_done
            else:
                dates = list(rrule.rrule(rrule.DAILY,
                                         dtstart=parser.parse(sheet.date_from),
                                         until=parser.parse(sheet.date_to)))
                ctx = dict(context)
                ctx.update(date_from=sheet.date_from,
                            date_to=sheet.date_to)

                for date_line in dates:
                    duty_hours = self.calculate_duty_hours(sheet.employee_id.id, date_line, context=ctx)
                    res[sheet.id]['total_duty_hours'] += duty_hours
                res[sheet.id]['total_duty_hours'] = res[sheet.id]['total_duty_hours'] - sheet.total_attendance
        return res

    @api.multi
    def count_leaves(self, date_from, employee_id, context=None):
        holiday_obj = self.env['hr.holidays']
        leaves = []
        start_leave_period = end_leave_period = False
        if context.get('date_from') and context.get('date_to'):
            start_leave_period = context.get('date_from')
            end_leave_period = context.get('date_to')
        holiday_ids = holiday_obj.search([('date_from','>=',start_leave_period),
                                          ('date_to','<=',end_leave_period),
                                          ('employee_id','=',employee_id),
                                          ('state','=','validate'),
                                          ('type','=','remove')])
        leaves = []

        for leave in holiday_obj.browse(cr, uid, holiday_ids, context=context):
            leave_date_from = datetime.strptime(leave.date_from, '%Y-%m-%d %H:%M:%S')
            leave_date_to = datetime.strptime(leave.date_to, '%Y-%m-%d %H:%M:%S')
            leave_dates = list(rrule.rrule(rrule.DAILY,
                                     dtstart=parser.parse(leave.date_from),
                                     until=parser.parse(leave.date_to)))
            for date in leave_dates:
                if date.strftime('%Y-%m-%d') == date_from.strftime('%Y-%m-%d'):
                    leaves.append((leave_date_from, leave_date_to))
                    break
        # END
        return leaves

    @api.multi
    def calculate_duty_hours(self, employee_id, date_from, context):
        contract_obj = self.env['hr.contract']
        calendar_obj = self.env['resource.calendar']
        duty_hours = 0.0
        contract_ids = contract_obj.search([('employee_id','=',employee_id),
                                            ('date_start','<=', date_from), '|',
                                            ('date_end', '>=', date_from),
                                            ('date_end', '=', None)],
                                            context=context)

        for contract in contract_obj.browse(contract_ids, context=context):
            dh = calendar_obj.get_working_hours_of_date(cr=cr, uid=uid,
                                                         id=contract.working_hours.id,
                                                         start_dt=date_from,
                                                         resource_id=employee_id, # Find leaves of this employee
                                                         context=context)

            leaves = self.count_leaves(date_from, employee_id, context=context)
            if not leaves:
                duty_hours += dh
        return duty_hours

    @api.multi
    def _get_overtime(self, start_date, context=None):
        for sheet in self.browse(ids, context):
            if sheet.state == 'done':
                return sheet.total_duty_hours_done * -1
            return self.calculate_diff(cr, uid, ids, start_date, context)

    @api.multi
    def _get_previous_month_diff(self, employee_id, prev_timesheet_date_from, context=None):
        total_diff = 0.0
        timesheet_ids = self.search([('employee_id','=',employee_id),
                                     ('date_from', '<', prev_timesheet_date_from), # Get only previous timesheets
                                     ])
        for timesheet in self.browse(timesheet_ids):
            total_diff += self._get_overtime([timesheet.id], start_date=prev_timesheet_date_from, context=context)
        return total_diff

    @api.multi
    @api.depends('prev_timesheet_diff','calculate_diff_hours')
    def _overtime_diff(self, name, args, context=None):
        res = {}
        for sheet in self.browse(cr, uid, ids, context):
            old_timesheet_start_from = parser.parse(sheet.date_from)-timedelta(days=1) ##entender porque foi montado dessa forma
            prev_timesheet_diff = self._get_previous_month_diff(sheet.employee_id.id,
                                                               old_timesheet_start_from.strftime('%Y-%m-%d'),
                                                               context=context)
            res.setdefault(sheet.id, {
                'calculate_diff_hours': self._get_overtime(ids,
                                                          datetime.today().strftime('%Y-%m-%d'),
                                                          context) + prev_timesheet_diff,
                'prev_timesheet_diff': prev_timesheet_diff,
            })
        return res

    @api.multi
    def write(self,vals):
        if 'state' in vals and vals['state'] == 'done':
            vals['total_diff_hours'] = self.calculate_diff(cr, uid, ids, None, context)
            for sheet in self.browse(cr, uid, ids, context=context):
                vals['total_duty_hours_done'] = sheet.total_duty_hours
        elif 'state' in vals and vals['state'] == 'draft':
            vals['total_diff_hours'] = 0.0
        res = super(TimeSheetComp, self).write(vals)
        return res

    def calculate_diff(self, cr, uid, ids, end_date=None, context=None):
        for sheet in self.browse(cr, uid, ids, context):
            return sheet.total_duty_hours * -1

    total_duty_hours = fields.Char(compute='_duty_hours', string='Total Duty Hours')
    total_duty_hours_done = fields.Float('Total Duty Hours', readonly=True, default=0.0)
    total_diff_hours = fields.Float('Total Diff Hours', readonly=True, default=0.0)
    calculate_diff_hours = fields.Char(compute='_overtime_diff', string="Diff (worked-duty)")
    prev_timesheet_diff = fields.Char(compute='_overtime_diff', string="Diff from old")
    comptime_analysis = fields.One2many('hr_timesheet_sheet.sheet.day', 'sheet_id', help='')

    @api.multi
    def intervalos(self):
        ff = tools.DEFAULT_SERVER_DATE_FORMAT
        start_dt = datetime.strptime(self.date_from, ff)
        end_dt = datetime.strptime(self.date_to, ff)

        calendar_obj = self.env['resource.calendar']
        calendar = calendar_obj.browse(1)
        working_hours = calendar.get_working_intervals_of_day(start_dt,
                                                            compute_leaves=True)
        import pdb; pdb.set_trace()
