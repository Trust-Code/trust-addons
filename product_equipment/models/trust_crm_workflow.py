# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class CrmHelpdeskType(models.Model):
    _name = "crm.helpdesk.type"
    _order = 'sequence'

    name = fields.Char(max_length=20, string="Nome do Estágio",
                       required=True)
    fold = fields.Boolean(string='Dobrado na Visão Kanban')
    sequence = fields.Integer(string="Sequência", default=1)
    count_time = fields.Boolean(string='Conta Tempo')


class CrmWorkflow(models.Model):
    _inherit = "crm.helpdesk"

    def _default_stage_id(self):
        stage = self.env["crm.helpdesk.type"].search([], limit=1,
                                                     order='sequence asc')
        return stage[0]

    stage_id = fields.Many2one(comodel_name='crm.helpdesk.type',
                               default=_default_stage_id)
