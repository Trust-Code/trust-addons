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
from openerp.exceptions import Warning as UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    segment = fields.Char(string="Segmento", size=30)
    attribute_ids = fields.One2many('crm.lead.attributes', 'lead_id',
                                    string="Atributos", )

    @api.multi
    def new_lead_via_api(self, lead, **post):
        source = self.env['crm.tracking.source'].search(
            [('unique_identifier', '=', post['origin'])])
        if source:
            lead['name'] = source.description + ' - ' + post['contact_name']
            lead['contact_name'] = post['contact_name']
            lead['email_from'] = post['email_from']
            lead['segment'] = post['company_segment']
            lead['source_id'] = source.id
            new_lead = self.create(lead)
            if source.mail_template_id:
                source.mail_template_id.send_mail(
                    new_lead.id,
                    force_send=True,
                    raise_exception=False)
        else:
            raise UserError('Atenção!', 'Identificador da origem desconhecido')


class CrmLeadAttributes(models.Model):
    _name = 'crm.lead.attributes'

    name = fields.Char('Nome', size=50)
    value = fields.Char('Valor', size=250)
    lead_id = fields.Many2one('crm.lead', string="Lead")


class CrmTrackinSource(models.Model):
    _inherit = 'crm.tracking.source'

    unique_identifier = fields.Char('Identificador', size=50)
    description = fields.Char('Descrição', size=100)
    mail_template_id = fields.Many2one(
        'email.template',
        string="Template de e-mail")
