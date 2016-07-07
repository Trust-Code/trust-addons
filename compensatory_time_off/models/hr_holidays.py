# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime, timedelta
from dateutil import rrule
from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    timesheet_sheet_id = fields.Many2one('hr_timesheet_sheet.sheet',
                                         string="Planilha de horas")

    total_duty_hours_off = fields.Float(string='Total de horas Folga')

    def onchange_date_from(self, cr, uid, ids, date_to,
                           date_from, employee_id, context=None):
        result = super(HrHolidays, self).onchange_date_from(
            cr, uid, ids, date_to, date_from)
        if date_to and date_from:
            hours = self._calc_off_hours(
                cr, uid, ids, date_from, date_to, employee_id)
            result['value']['total_duty_hours_off'] = hours
        return result

    def onchange_date_to(self, cr, uid, ids, date_to,
                         date_from, employee_id, context=None):
        result = super(HrHolidays, self).onchange_date_to(
            cr, uid, ids, date_to, date_from)
        if date_to and date_from:
            hours = self._calc_off_hours(
                cr, uid, ids, date_from, date_to, employee_id)
            result['value']['total_duty_hours_off'] = hours
        return result

    def _calc_off_hours(self, cr, uid, ids, date_from, date_to, employee_id):
        date_from = datetime.strptime(date_from, DATETIME_FORMAT)
        date_to = datetime.strptime(date_to, DATETIME_FORMAT)

        days = list(rrule.rrule(
            rrule.DAILY, dtstart=date_from,
            until=(date_to + timedelta(days=1)).replace(
                hour=0, minute=0, second=0)))

        total = 0.0
        contract_ids = self.pool['hr.contract'].search(
            cr, uid,
            [('employee_id', '=', employee_id),
             ('date_start', '<=', date.today().strftime(DATE_FORMAT)),
             '|', ('date_end', '>=', date.today().strftime(DATE_FORMAT)),
             ('date_end', '=', None)])
        contract = self.pool['hr.contract'].browse(cr, uid, contract_ids[0])
        calendar = contract.working_hours

        total_days = len(days)
        index = 1
        for day in days:
            start = day.replace(hour=0, minute=0, second=0)
            to = day.replace(hour=23, minute=59, second=59)
            if index == 1:
                start = start.replace(hour=date_from.hour,
                                      minute=date_from.minute,
                                      second=date_from.second)
            if index == total_days:
                to = to.replace(hour=date_to.hour,
                                minute=date_to.minute,
                                second=date_to.second)

            total += calendar.get_working_hours_of_date(
                start_dt=start, end_dt=to, compute_leaves=True)[0]

            index += 1
        return total

    @api.multi
    def write(self, values):
        self.ensure_one()
        state = self.state
        if "state" in values:
            state = values["state"]
        if state != 'validate':
            date_from = self.date_from
            date_to = self.date_to
            employee_id = self.employee_id.id
            if "date_from" in values:
                date_from = values["date_from"]
            if "date_to" in values:
                date_to = values["date_to"]
            if "employee_id" in values:
                employee_id = values["employee_id"]

            values['total_duty_hours_off'] = self._calc_off_hours(
                date_from, date_to, employee_id)
        return super(HrHolidays, self).write(values)
