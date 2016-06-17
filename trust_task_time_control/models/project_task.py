# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
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

    def count_time_start(self, stage_name, user_id):
        df = tools.DEFAULT_SERVER_DATETIME_FORMAT
        self.env['project.task.work'].create(
            {'name': u'Tempo Automático (%s)' % (stage_name),
             'task_id': self.id,
             'date': datetime.now().strftime(df),
             'user_id': user_id,
             'hours': 0.0,
             'time_open': True,
             'time_control': True})
        return

    def count_time_stop(self, user_id):
        task_work = self.env['project.task.work'].search(
            [('user_id', '=', user_id),
             ('time_open', '=', True)],
            order='id desc', limit=1)

        if task_work:
            ff = tools.DEFAULT_SERVER_DATETIME_FORMAT
            count_time = datetime.now() - datetime.strptime(task_work.date, ff)

            task_work.hours = count_time.total_seconds() / 60.0 / 60.0
            task_work.time_open = False
        return

    def presence_state(self, user_id):
        state = False
        presence = self.env['hr.attendance'].search(
            [('employee_id.user_id', '=', user_id)],
            order='id desc', limit=1)

        if presence.action == 'sign_in':
            state = True
        return state

    def other_task_time_open(self, user_id):
        state = False
        other_time_open = self.env['project.task.work'].search(
            [('user_id', '=', user_id),
             ('time_open', '=', True)],
            order='id desc', limit=1)

        if other_time_open.time_open and other_time_open.task_id.id != self.id:
            state = True
        return state

    @api.multi
    def write(self, vals):
        if "stage_id" in vals:
            next_stage = self.env['project.task.type'].browse(vals["stage_id"])
            if next_stage.count_time:
                if self.other_task_time_open(self.user_id.id):
                    raise Warning(u"Movimentação não Permitida!",
                                  u"Já existe outra tarefa em contando tempo.")
                else:
                    self.count_time_stop(self.user_id.id)
                    if self.presence_state(self.user_id.id):
                        self.count_time_start(next_stage.name, self.user_id.id)
            else:
                self.count_time_stop(self.user_id.id)

        elif "kanban_state" in vals:
            if vals["kanban_state"] == "blocked":
                self.count_time_stop(self.user_id.id)
            elif vals["kanban_state"] == "normal" and\
                    self.presence_state(self.user_id.id):
                if self.other_task_time_open(self.user_id.id):
                    raise Warning(u"Alteração não Permitida!",
                                  u"Já existe outra tarefa contando tempo.")
                else:
                    self.count_time_start(self.stage_id.name, self.user_id.id)
        elif "user_id" in vals and self.stage_id.count_time:
            self.count_time_stop(self.user_id.id)

        return super(ProjectTask, self).write(vals)


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    count_time = fields.Boolean('Count Time')


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    time_open = fields.Boolean('Time Open')
    time_control = fields.Boolean('Time Control')
