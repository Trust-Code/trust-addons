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


class CrmHelpesk(models.Model):
    _inherit = 'crm.helpdesk'

    def _default_email_from(self):
        if "default_trustcode_solicitation" in self.env.context:
            return self.env.user.partner_id.email or self.env.user.login

    responsible = fields.Char('Atendente', readonly=True, size=50)
    trustcode_solicitation = fields.Boolean("Chamado Trustcode")
    email_from = fields.Char("Email", size=128, default=_default_email_from)

    @api.model
    def create(self, vals):
        self.send_to_trustcode()
        return super(CrmHelpesk, self).create(vals)

    @api.multi
    def send_to_trustcode(self):
        pass

    @api.model
    def synchronize_helpdesk_solicitation(self):
        solicitations = self.search([('trustcode_solicitation', '=', True),
                                     ('state', '!=', 'done'),
                                     ('state', '!=', 'cancel')])
        for solicitation in solicitations:

            print solicitation.trustcode_id


class CrmHelpdeskInteraction(models.Model):
    _inherit = 'crm.helpdesk.interaction'

    responsible = fields.Char(u'Atendente', size=50, readonly=True)
    trustcode_solicitation = fields.Boolean(
        "Chamado Trustcode", related="crm_help_id.trustcode_solicitation")
