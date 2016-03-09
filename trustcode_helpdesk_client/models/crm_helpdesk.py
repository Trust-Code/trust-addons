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
import odoorpc


class CrmHelpesk(models.Model):
    _name = 'crm.helpdesk.trustcode'
    _description = "Chamados Trustcode"
    _order = "id desc"
    _inherit = ['mail.thread']

    def _default_email_from(self):
        return self.env.user.partner_id.email or self.env.user.login

    def _default_company(self):
        return self.env.user.company_id.id

    trustcode_id = fields.Char(u"Id Único", size=80)
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=_default_company)
    date_closed = fields.Datetime('Closed', readonly=True)
    email_from = fields.Char('Email', size=128,
                             help="Destination email for email gateway",
                             default=_default_email_from)
    date = fields.Datetime(
        'Date',
        readonly=True,
        default=fields.Datetime.now())
    priority = fields.Selection(
        [('0', 'Low'), ('1', 'Normal'), ('2', 'High')], 'Priority')
    state = fields.Selection(
        [('draft', 'Novo'),
         ('open', 'Em progresso'),
         ('pending', 'Pendente'),
         ('done', 'Fechado'),
         ('cancel', 'Cancelado')], 'Status',
        readonly=True, track_visibility='onchange',
        default='draft',
    )
    responsible = fields.Char('Atendente', readonly=True, size=50)
    responsible_id = fields.Many2one(
        'res.users',
        string='Atendente',
        readonly=True,
        size=50)
    attachment = fields.Binary(u'Anexo')
    version = fields.Integer(u'Versão', default=0)
    interaction_ids = fields.One2many(
        'crm.helpdesk.trustcode.interaction',
        'crm_help_id', string="Interações")

    @api.model
    def create(self, vals):
        self.send_to_trustcode(vals)
        return super(CrmHelpesk, self).create(vals)

    @api.multi
    def send_to_trustcode(self, vals):
        url = self.env.user.company_id.url_trustcode
        cnpj = self.env.user.company_id.cnpj_cpf
        odoo = odoorpc.ODOO(url, port=8069)
        vals['cnpj'] = cnpj
        r = odoo.json('/helpdesk/new', vals)
        vals['trustcode_id'] = r['result']['trustcode_id']

    @api.model
    def synchronize_helpdesk_solicitation(self):
        env_inter = self.env['crm.helpdesk.trustcode.interaction']
        url = self.env.user.company_id.url_trustcode
        cnpj = self.env.user.company_id.cnpj_cpf
        odoo = odoorpc.ODOO(url, port=8069)
        result = odoo.json('/helpdesk/list', {'cnpj': cnpj})
        if result['result']['sucesso']:
            for item in result['result']['solicitations']:
                help_sol = self.search(
                    [('trustcode_id', '=', item['trustcode_id'])])
                if help_sol:
                    help_sol.state = item['state']
                    help_sol.responsible = item['responsible']
                    help_sol.priority = item['priority']
                    for interact in item['interactions']:
                        inter = env_inter.search(
                            [('trustcode_id', '=', interact['trustcode_id'])])
                        if inter:
                            inter.state = interact['state']
                            inter.name = interact['name']
                            inter.responsible = interact['responsible']
                            inter.time_since_last_interaction = interact[
                                'time_since_last_interaction']
                        else:
                            interact['crm_help_id'] = help_sol.id
                            int_env = self.env[
                                'crm.helpdesk.trustcode.interaction']
                            int_env.create(interact)


class CrmHelpdeskInteraction(models.Model):
    _name = 'crm.helpdesk.trustcode.interaction'
    _description = u'Interações do chamado'

    def _default_responsible(self):
        return self.env.user.id

    trustcode_id = fields.Char(u"Id Único", size=80)
    date = fields.Datetime(u'Data', default=fields.Datetime.now())
    time_since_last_interaction = fields.Float(u'Última interação')
    state = fields.Selection([('new', 'Novo'), ('read', 'Lida')],
                             u'Status', default='new')
    name = fields.Text(string=u'Resposta')
    crm_help_id = fields.Many2one('crm.helpdesk.trustcode', string=u"Chamado")
    attachment = fields.Binary(u'Anexo')
    responsible = fields.Char(u'Atendente', size=50, readonly=True)
    responsible_id = fields.Many2one(
        'res.users', string='Atendente',
        readonly=True, size=50, default=_default_responsible)

    @api.multi
    def mark_as_read(self):
        url = self.env.user.company_id.url_trustcode
        for item in self:
            if not item.responsible_id:
                item.write({'state': 'read'})
                odoo = odoorpc.ODOO(url, port=8069)
                odoo.json('/helpdesk/interaction/update',
                          {'trustcode_id': item.trustcode_id,
                           'user': self.env.user.name})

    @api.model
    def create(self, vals):
        if "trustcode_id" not in vals:
            self.send_to_trustcode(vals)
        return super(CrmHelpdeskInteraction, self).create(vals)

    @api.multi
    def send_to_trustcode(self, vals):
        url = self.env.user.company_id.url_trustcode
        cnpj = self.env.user.company_id.cnpj_cpf
        odoo = odoorpc.ODOO(url, port=8069)
        help_id = self.env['crm.helpdesk.trustcode'].browse(
            vals['crm_help_id'])
        vals['help_trustcode_id'] = help_id.trustcode_id
        vals['cnpj'] = cnpj
        r = odoo.json('/helpdesk/interaction/new', vals)
        vals['trustcode_id'] = r['result']['trustcode_id']
