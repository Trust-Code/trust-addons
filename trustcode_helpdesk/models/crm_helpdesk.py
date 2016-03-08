# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 TrustCode - www.trustcode.com.br                         #
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


import uuid
from openerp import api, fields, models


class CrmHelpdeskInteraction(models.Model):
    _name = 'crm.helpdesk.interaction'
    _description = u'Interações do chamado'

    def _default_responsible(self):
        return self.env.user.partner_id.id

    responsible_id = fields.Many2one('res.partner', u'Responsável',
                                     default=_default_responsible)
    date = fields.Datetime(u'Data', default=fields.Datetime.now())
    time_since_last_interaction = fields.Float(u'Última interação')
    state = fields.Selection([('new', 'Novo'), ('read', 'Lida')],
                             u'Status', default='new')
    name = fields.Text(string=u'Resposta')
    crm_help_id = fields.Many2one('crm.helpdesk', string=u"Chamado")
    attachment = fields.Binary(u'Anexo')
    trustcode_id = fields.Char(u"Id Único", size=80)

    @api.multi
    def mark_as_read(self):
        self.write({'state': 'read'})


class CrmHelpDesk(models.Model):
    _inherit = 'crm.helpdesk'

    trustcode_id = fields.Char(u"Id Único", size=80)
    attachment = fields.Binary(u'Anexo')
    interaction_ids = fields.One2many(
        'crm.helpdesk.interaction',
        'crm_help_id', string="Interações")

    @api.multi
    def new_solicitation_api(self, **kwargs):
        kwargs.update({'trustcode_id': str(uuid.uuid4())})
        self.create(kwargs)
        return kwargs['trustcode_id']

    @api.multi
    def new_interaction(self, **kwargs):
        helpdesk = self.search(
            [('trustcode_id', '=', kwargs['help_trustcode_id'])])
        if helpdesk:
            kwargs['crm_help_id'] = helpdesk.id
            kwargs.update({'trustcode_id': str(uuid.uuid4())})
            self.env['crm.helpdesk.interaction'].create(kwargs)
            return kwargs['trustcode_id']

    @api.multi
    def update_interaction(self, **kwargs):
        interaction = self.env['crm.helpdesk.interaction'].search(
            [('trustcode_id', '=', kwargs['trustcode_id'])])

        interaction.mark_as_read()
