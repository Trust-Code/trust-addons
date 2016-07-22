# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# TODO testar escalonador e wizard na base pelican

from datetime import date, timedelta
from openerp import api, fields, models


class escalonador_wizard(models.TransientModel):
    _name = 'escalonador.wizard'

    @api.one
    def escalonador(self):
        employees = self.env['hr.employee'].search([
            ('tasks_categ', '!=', False)])
        open_tasks = self.env['project.task'].search(
            [('stage_id.closed', '=', False),
             ('stage_id.cancelled_state', '=', False),
             ('user_id', '=', False)],
            order='priority desc, create_date asc')
        employee_count = len(employees) - 1
        indice_funcionario = 0
        categ_check = True
        tomorrow = (date.today() + timedelta(days=1))
        for task in open_tasks:
            while not task.user_id:
                for i in task.categ_ids:
                    categ_bool = i in employees[indice_funcionario].\
                        tasks_categ
                    categ_check = categ_check and categ_bool
                if categ_check:
                    task.write(
                        {'user_id': employees[indice_funcionario].user_id.id,
                         'date_deadline': tomorrow})
                indice_funcionario += 1
                categ_check = True
                if indice_funcionario == employee_count:
                    indice_funcionario = 0
