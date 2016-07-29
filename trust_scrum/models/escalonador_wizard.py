# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta
from openerp import api, models


class escalonador_wizard(models.TransientModel):
    _name = 'escalonador.wizard'

    @api.one
    def escalonador(self):
        def assert_weekday(date):
            if date.isoweekday() >= 6:
                while date.isoweekday() != 1:
                    date += timedelta(days=1)
            return date
        employees = self.env['hr.employee'].search([
            ('id', '!=', 1)])
        open_tasks = self.env['project.task'].search(
            [('stage_id.closed', '=', False),
             ('stage_id.cancelled_state', '=', False),
             ('stage_id.count_time', '=', False),
             ('user_id', '=', False)],
            order='priority desc, create_date asc').ids
        day = datetime.today().day
        month = datetime.today().month
        year = datetime.today().year
        date_start = datetime(year, month, day, 0, 0, 0)
        date_end = datetime(year, month, day, 23, 59, 59)
        categ_check = True
        lista_tarefas = open_tasks
        while(len(lista_tarefas) > 0):
            date_start = assert_weekday(date_start)
            date_end = assert_weekday(date_end)
            for employee in employees:
                for task_id in lista_tarefas:
                    task = self.env['project.task'].browse(task_id)
                    if not task.categ_ids:
                        task.write({'user_id': employee.user_id.id,
                                    'date_start': date_start +
                                    timedelta(hours=3),
                                    'date_end': date_end +
                                    timedelta(hours=3)})
                    else:
                        for i in task.categ_ids:
                            categ_bool = i in employee.tasks_categ
                            categ_check = categ_check and categ_bool
                        if categ_check:
                            task.write({'user_id': employee.user_id.id,
                                        'date_start': date_start +
                                        timedelta(hours=3),
                                        'date_end': date_end +
                                        timedelta(hours=3)})
                        else:
                            task.write({'user_id': employee.user_id.id,
                                        'date_start': date_start +
                                        timedelta(hours=3),
                                        'date_end': date_end +
                                        timedelta(hours=3)})
                    break
                if task_id in lista_tarefas:
                    lista_tarefas.remove(task_id)
            date_start += timedelta(days=1)
            date_end += timedelta(days=1)
