# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    task_id = fields.Many2one('project.task', string="Tarefa")
