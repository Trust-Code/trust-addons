# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
#              Mackilem Van der Lan <mack.vdl@gmail.com>                      #
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
#                                                                             #
###############################################################################


from openerp import api, fields, models, tools
from datetime import datetime
from openerp.exceptions import Warning


class ProjectTask (models.Model):
    _inherit = 'project.task'

    def count_time_start(self, stage_name):
        df = tools.DEFAULT_SERVER_DATETIME_FORMAT
        self.env['project.task.work'].create(
            {'name': 'Tempo Automatico (%s)' % (stage_name),
             'task_id': self.id,
             'date': datetime.now().strftime(df),
             'user_id': self.env.user.id,
             'hours': 0.0,
             'time_open': True,
             'time_control': True})
        return

    def count_time_stop(self):
        task_work = self.env['project.task.work'].search(
            [('user_id', '=', self.env.user.id),
             ('time_open', '=', True)],
            order='id desc', limit=1)

        if task_work:
            ff = tools.DEFAULT_SERVER_DATETIME_FORMAT
            count_time = datetime.now() - datetime.strptime(task_work.date, ff)

            task_work.hours = count_time.total_seconds() / 60.0 / 60.0
            task_work.time_open = False
        return

    def presence_state(self):
        state = False
        presence = self.env['hr.attendance'].search(
            [('employee_id.user_id', '=', self.env.user.id)],
            order='id desc', limit=1)

        if presence.action == 'sign_in':
            state = True
        return state

    def other_task_time_open(self):
        state = False
        other_time_open = self.env['project.task.work'].search(
            [('user_id', '=', self.env.user.id),
             ('time_open', '=', True)],
            order='id desc', limit=1)

        if other_time_open and other_time_open.task_id.id != self.id:
            state = True
        return state

    @api.multi
    def write(self, vals):
        if "stage_id" in vals:
            next_stage = self.env['project.task.type'].browse(vals["stage_id"])
            if next_stage.count_time:
                if self.other_task_time_open():
                    raise Warning(u"Movimentação não Permitida!",
                                  u"Já exite outra tarefa em contando tempo.")

                else:
                    self.count_time_stop()

                    if self.presence_state():
                        self.count_time_start(next_stage.name)
            else:
                self.count_time_stop()

        elif "kanban_state" in vals:
            if vals["kanban_state"] == "blocked":
                self.count_time_stop()

            elif vals["kanban_state"] == "normal" and self.presence_state():
                if self.other_task_time_open():
                    raise Warning(u"Movimentação não Permitida!",
                                  u"Já exite outra tarefa em contando tempo.")
                else:
                    self.count_time_start(self.stage_id.name)

        return super(ProjectTask, self).write(vals)


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    count_time = fields.Boolean('Count Time')


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    time_open = fields.Boolean('Time Open')
    time_control = fields.Boolean('Time Control')
