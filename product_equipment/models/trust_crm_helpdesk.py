# -*- encoding: utf-8 -*-
# © 2016 Alessandro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    phone = fields.Char(max_length=30, string="Telefone")
    mobile = fields.Char(max_length=30, string="Celular")
    equip_tag = fields.Many2one(comodel_name='product.template',
                                inverse_name='tag',
                                string="Etiqueta do Equip.")
    att_description = fields.Text()
    priority = fields.Selection([('0', 'Baixa'),
                                 ('1', 'Normal'),
                                 ('2', 'Média'),
                                 ('3', 'Alta')],
                                string="Prioridade")

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
