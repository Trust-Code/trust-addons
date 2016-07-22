# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _open_meeting_count(self):
        for meeting in self:
            count = self.env['calendar.event'].search_count([
                ('task_id', '=', meeting.id)
            ])
            meeting.meeting_count = count

    meeting_count = fields.Integer(string="Reuniões",
                                   compute="_open_meeting_count")
