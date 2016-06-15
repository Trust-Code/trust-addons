# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 Trustcode - www.trustcode.com.br                         #
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
    responsible = fields.Char('Atendente', readonly=True, size=50)
    date = fields.Datetime(u'Data', default=fields.Datetime.now())
    time_since_last_interaction = fields.Float(u'Última interação')
    state = fields.Selection([('new', 'Novo'), ('read', 'Lida')],
                             u'Status', default='new')
    name = fields.Text(string=u'Resposta')
    crm_help_id = fields.Many2one('crm.helpdesk', string=u"Chamado")
    attachment = fields.Binary(u'Anexo')
    trustcode_id = fields.Char(u"Id Único", size=80,
                               default=lambda *args: str(uuid.uuid4()))
    interacao_trustcode = fields.Boolean(
        u"Interação do suporte",
        default=True)

    @api.multi
    def mark_as_read(self):
        for item in self:
            if not item.interacao_trustcode:
                item.write({'state': 'read'})

    @api.model
    def create(self, vals):
        result = super(CrmHelpdeskInteraction, self).create(vals)
        if result.interacao_trustcode:
            helpdesk = self.env['crm.helpdesk'].browse(vals['crm_help_id'])
            helpdesk.partner_id.message_post(
                type='email',
                subject=u"Nova interação no chamado %s" % helpdesk.name,
                body=vals['name'])

            template_id = self.env['ir.model.data'].get_object_reference(
                'trustcode_helpdesk', 'email_template_nova_interacao')[1]
            mail_template = self.env['email.template'].browse(
                template_id)
            mail_template.send_mail(
                result.id, force_send=False, raise_exception=False)
        return result


class CrmHelpDesk(models.Model):
    _inherit = 'crm.helpdesk'

    trustcode_id = fields.Char(u"Id Único", size=80)
    attachment = fields.Binary(u'Anexo')
    interaction_ids = fields.One2many(
        'crm.helpdesk.interaction',
        'crm_help_id', string="Interações")

    def validate_cnpj(self, **kwargs):
        if "cnpj" in kwargs:
            partner = self.env['res.partner'].search(
                [('cnpj_cpf', '=', kwargs['cnpj'])])
            if partner:
                return partner
            else:
                raise Warning('Atenção!',
                              'Empresa não configurada na base da Trustcode')
        else:
            raise Warning('Atenção!',
                          'Configure seu CNPJ corretamente')

    @api.multi
    def new_solicitation_api(self, **kwargs):
        partner = self.validate_cnpj(**kwargs)
        kwargs.update({'trustcode_id': str(uuid.uuid4()),
                       'partner_id': partner.id,
                       'user_id': None})
        self.create(kwargs)
        users = self.env['res.users'].search(
            [('receive_support', '=', True)])
        for user in users:
            user.message_post(
                type='email',
                subject=u"Nova chamado %s" % kwargs['name'],
                body=kwargs['name'])
        return kwargs['trustcode_id']

    @api.multi
    def new_interaction(self, **kwargs):
        helpdesk = self.search(
            [('trustcode_id', '=', kwargs['help_trustcode_id'])])
        if helpdesk:
            kwargs.update({'trustcode_id': str(uuid.uuid4()),
                           'crm_help_id': helpdesk.id,
                           'interacao_trustcode': False})
            self.env['crm.helpdesk.interaction'].create(kwargs)
            if helpdesk.user_id:
                helpdesk.user_id.message_post(
                    type='email',
                    subject=u"Nova interação no chamado %s" % helpdesk.name,
                    body=kwargs['name'])
            return kwargs['trustcode_id']

    @api.multi
    def update_interaction(self, **kwargs):
        interaction = self.env['crm.helpdesk.interaction'].search(
            [('trustcode_id', '=', kwargs['trustcode_id'])])

        interaction.state = 'read'
        body = "Interação lida por - %s" % kwargs['user']
        interaction.crm_help_id.message_post(type='notification',
                                             subtype="mt_comment",
                                             body=body)

    @api.multi
    def list_solicitation(self, **kwargs):
        partner = self.validate_cnpj(**kwargs)
        solicitations = self.env['crm.helpdesk'].search(
            [('state', 'in', ('open', 'pending')),
             ('partner_id', '=', partner.id)])

        items = []

        for solicitation in solicitations:
            item = {'trustcode_id': solicitation.trustcode_id,
                    'name': solicitation.name,
                    'responsible': solicitation.user_id.name,
                    'state': solicitation.state,
                    'priority': solicitation.priority,
                    'description': solicitation.description,
                    'interactions': []}

            for interaction in solicitation.interaction_ids.sorted(
                    lambda x: x.id):
                interact = {
                    'trustcode_id': interaction.trustcode_id,
                    'name': interaction.name,
                    'responsible':
                    ("Suporte - %s" % interaction.responsible_id.name)
                    if interaction.interacao_trustcode
                    else interaction.responsible,
                    'state': interaction.state,
                    'date': interaction.date,
                    'interacao_trustcode': interaction.interacao_trustcode,
                    'time_since_last_interaction':
                    interaction.time_since_last_interaction
                }

                item['interactions'].append(interact)

            items.append(item)

        return items
