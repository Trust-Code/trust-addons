# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
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
###############################################################################

from openerp import api, models, fields


class wizard(models.TransientModel):
    _name = 'multi.call'

    res_user_id = fields.Many2many('res.users', string="Atendentes")

    @api.multi
    def create_calls(self):
        customers = self._context.get('active_ids')
        customers_ids = self.env['res.partner'].browse(customers)

        cpu = len(customers_ids) / len(self.res_user_id)
        indice_usuario = 0
        somador = 0
        for c in customers_ids:
            crm_phonecall = self.env['crm.phonecall']
            crm_phonecall.create({
                'name': c.category_id.name,
                'partner_phone': '%s-%s-%s-%s' % (c.phone, c.mobile,
                                                  c.x_phone1, c.fax),
                'partner_id': c.id,
                'user_id': self.res_user_id[indice_usuario].id
            })

            somador += 1
            if somador >= cpu and indice_usuario < len(self.res_user_id) - 1:
                indice_usuario += 1
                somador = 0
