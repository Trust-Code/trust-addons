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


from openerp import api, fields, models


class CrmHelpdeskInteraction(models.Model):
    _name = 'crm.helpdesk.interaction'
    _description = u'Interações do chamado'

    def _default_responsible(self):
        return self.env.user.partner_id.id

    trustcode_id = fields.Char(u"Id Único", size=80)
    responsible_id = fields.Many2one('res.partner', u'Responsável',
                                     default=_default_responsible)
    date = fields.Datetime(u'Data', default=fields.Datetime.now())
    time_since_last_interaction = fields.Float(u'Última interação')
    state = fields.Selection([('new', 'Novo'), ('read', 'Lida')],
                             u'Status', default='new')
    name = fields.Text(string=u'Resposta')
    crm_help_id = fields.Many2one('crm.helpdesk', string=u"Chamado")
    attachment = fields.Binary(u'Anexo')

    @api.multi
    def mark_as_read(self):
        self.write({'state': 'read'})


class CrmHelpDesk(models.Model):
    _inherit = 'crm.helpdesk'

    attachment = fields.Binary(u'Anexo')
    version = fields.Integer(u'Versão', default=0)
    interaction_ids = fields.One2many(
        'crm.helpdesk.interaction',
        'crm_help_id', string="Interações")

    @api.multi
    def write(self, vals):
        for item in self:
            item.version += 1
        return super(CrmHelpDesk, self).write(vals)
