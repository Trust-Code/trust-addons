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


import time
from openerp.tests import common
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from mock import patch


class TestTaskTime(common.TransactionCase):

    def setUp(self):
        super(TestTaskTime, self).setUp()
        self.project = self.env['project.project'].create(
            {'name': 'Test Project'})

        self.task_one = self.env['project.task'].create({'name': 'task one',
                                                         'project_id': self.project.id})

        self.task_two = self.env['project.task'].create({'name': 'task two',
                                                         'project_id': self.project.id})

        self.stage_running = self.env.ref('project.project_tt_deployment')
        self.stage_running.count_time = True
        self.employee = self.env['hr.employee'].browse(self.env.user.id)

    def test_create_task_work(self):
        self.employee.attendance_action_change()
        self.assertEqual(self.employee.state, 'present',
                         'Não registrou corretamente entrada do usuário')

        self.assertEqual(len(self.task_one.work_ids), 0,
                         'Registrou trabalho em uma tarefa que não conta tempo')
        self.assertEqual(len(self.task_two.work_ids), 0,
                         'Registrou trabalho em uma tarefa que não conta tempo')

        self.task_one.stage_id = self.stage_running.id

        self.assertEqual(len(self.task_one.work_ids), 1,
                         'Não registrou o tempo na tarefa um')
        self.assertEqual(len(self.task_two.work_ids), 0,
                         'Registrou trabalho em uma tarefa que não conta tempo')
