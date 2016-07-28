# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class DanfseReport(models.AbstractModel):
    _name = 'report.trust_scrum.report_project_task'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'trust_scrum.report_project_task')
        hour_count = 0
        tasks = self.env['project.task'].search([('id', 'in', self.ids)])
        for task in tasks:
            hour_count += task.effective_hours

        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self.env[report.model].browse(self._ids),
            'hours': hour_count
        }
        return report_obj.render(
            'trust_scrum.report_project_task', docargs)
