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
        scrum_team = self.env['project.scrum.team'].search([], limit=1)
        team_ids = scrum_team.members.ids
        open_tasks = self.env['project.task'].search(
            [('stage_id.closed', '=', False),
             ('stage_id.cancelled_state', '=', False),
             ('stage_id.count_time', '=', False)],
            order='priority desc, create_date asc').ids
        day = datetime.today().day
        month = datetime.today().month
        year = datetime.today().year
        date_start = datetime(year, month, day, 0, 0, 0)
        date_end = datetime(year, month, day, 23, 59, 59)
        lista_tarefas = open_tasks
        while(len(lista_tarefas) > 0):
            date_start = assert_weekday(date_start)
            date_end = assert_weekday(date_end)
            for user in scrum_team.members:
                for task_id in lista_tarefas:
                    task = self.env['project.task'].browse(task_id)
                    user_id = user.id
                    if task.user_id.id in team_ids:
                        user_id = task.user_id.id
                    task.write({'user_id': user_id,
                                'date_start': date_start +
                                timedelta(hours=3),
                                'date_end': date_end +
                                timedelta(hours=3)})
                    break
                if task_id in lista_tarefas:
                    lista_tarefas.remove(task_id)
            date_start += timedelta(days=1)
            date_end += timedelta(days=1)
