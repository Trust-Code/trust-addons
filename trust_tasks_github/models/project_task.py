# -*- encoding: utf-8 -*-
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


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def _url_github(self):
        for item in self:
            item.link_issue = 'http://github.com/%s/%s/%s/%s' %\
                (item.repository.owner_name,
                 item.repository.repo_name,
                 ('issues' if item.type == 'issue' else 'pull'),
                 item.issue_github)

    repository = fields.Many2one('github.integration', string=u"Repositório")

    issue_github = fields.Char(u'Número github')
    type = fields.Selection([('issue', 'Issue'), ('pr', 'Pull Request')],
                            u'Tipo')
    link_issue = fields.Char(u'Link Issue', compute='_url_github',
                             readonly=True)
