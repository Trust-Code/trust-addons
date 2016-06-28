# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def draft_respartner(self):
        self.write({
            'stage_id': 'draft',
        })

    @api.one
    def hold_respartner(self):
        self.write({
            'stage_id': 'hold',
        })

    @api.one
    def confirmed_respartner(self):
        self.write({
            'stage_id': 'confirmed',
        })

    stage_id = fields.Selection([
        ('draft', 'Rascunho'),
        ('hold', 'Aguardando Verificação'),
        ('confirmed', 'Confirmado'),
    ], default='draft')

    @api.multi
    def write(self, vals):
        if 'stage_id' in vals and vals['stage_id'] == 'confirmed':
            error_list = []
            if not self.cnpj_cpf:
                error = "CPF/CNPJ não preenchido."
                error_list.append(error)
            if not self.zip:
                error = "CEP não preenchido."
                error_list.append(error)
            if not self.street:
                error = "Logradouro não preenchido."
                error_list.append(error)
            if not self.number:
                error = "Número não preenchido."
                error_list.append(error)
            if not self.district:
                error = "Bairro não preenchido."
                error_list.append(error)
            if not self.country_id:
                error = "País não preenchido."
                error_list.append(error)
            if not self.state_id:
                error = "Estado não preenchido."
                error_list.append(error)
            if not self.l10n_br_city_id:
                error = "Cidade não preenchida."
                error_list.append(error)
            if not self.phone:
                error = "Telefone não preenchido."
                error_list.append(error)
            if not self.email:
                error = "E-mail não preenchido."
                error_list.append(error)
            if len(error_list) > 0:
                raise UserError('Os seguintes campos não foram preenchidos:',
                                '\n'.join(error_list))
        return super(ResPartner, self).write(vals)
