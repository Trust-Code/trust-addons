# -*- encoding: utf-8 -*-
# © 2016 Alessandro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CrmHelpdeskType(models.Model):
    _name = "crm.helpdesk.type"
    _order = 'sequence'

    name = fields.Char(max_length=20, string="Nome do Estágio",
                       required=True)
    sequence = fields.Integer(string="Sequência", default=1)
    count_time = fields.Boolean(string='Conta Tempo')
    finished = fields.Boolean(string='Finalizado')


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    def _default_stage_id(self):
        stage = self.env["crm.helpdesk.type"].search([], limit=1,
                                                     order='sequence asc')
        return stage and stage[0]

    sequence = fields.Char(string="Sequência", size=20)
    phone = fields.Char(max_length=30, string="Telefone")
    mobile = fields.Char(max_length=30, string="Celular")
    equip_tag = fields.Many2one(comodel_name='product.template',
                                inverse_name='tag',
                                string="Etiqueta do Equip.")
    att_description = fields.Text(string="Descrição")
    priority = fields.Selection([('0', 'Baixa'),
                                 ('1', 'Normal'),
                                 ('2', 'Média'),
                                 ('3', 'Alta')],
                                string="Prioridade")
    date_deadline = fields.Datetime('Prazo Final')

    stage_id = fields.Many2one(comodel_name='crm.helpdesk.type',
                               default=_default_stage_id, string="Estágio")

    @api.model
    def create(self, vals):
        dummy, sequence_id = self.env['ir.model.data'].get_object_reference(
            'crm_helpdesk_workflow', 'sequence_crm_helpdesk')
        vals['sequence'] = self.env['ir.sequence'].next_by_id(sequence_id)
        return super(CrmHelpdesk, self).create(vals)

    @api.multi
    def equipment_history(self):
        action = self.env['ir.model.data'].\
            get_object('crm_helpdesk', 'crm_case_helpdesk_act111')

        return{
            'id': action.id,
            'name': action.name,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'res_model': action.res_model,
            'type': action.type,
            'domain': action.domain,
            'context': {'search_default_equip_tag': self.equip_tag.id}
        }
