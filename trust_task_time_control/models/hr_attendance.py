# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
#              Danimar Ribeiro <danimaribeiro@gmail.com>                      #
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

from openerp import api, fields, models
from openerp.exceptions import Warning


class HrAttendance (models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def attendance_action_change(self):
        running_tasks = self.env['project.task'].search(
            [('user_id', '=', self.env.user.id),
             ('stage_id.count_time', '=', True)],
            order='id desc', limit=1)
        if len(running_tasks) > 1:
            raise Warning(u"Entrada não Permitida!",
                          u"Existem duas tarefas no estágio em andamento.")
        if len(running_tasks) == 1:
            task = running_tasks[0]
            task.count_time_stop()

            if self.state == 'absent':
                task.count_time_start(task.stage_id.name)

        return super(HrAttendance, self).attendance_action_change()
