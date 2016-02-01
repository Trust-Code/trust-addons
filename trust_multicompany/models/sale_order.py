# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
#              Mackilem Van der Lan <mack.vdl@gmail.com>                      #
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


from openerp import api, fields, models, tools
from openerp.exceptions import Warning


class SaleMulticompany (models.Model):
    _inherit = 'sale.order'

    @api.multi
    def onchange_company_id(self, company_id, partner_id, partner_invoice_id,
                            partner_shipping_id):

        result = super(SaleMulticompany, self).onchange_company_id(
            company_id, partner_id, partner_invoice_id, partner_shipping_id)

        company = self.env['res.company'].browse(company_id)
        if company.out_invoice_fiscal_category_id:
            result['value'][
                'fiscal_category_id'] = company.out_invoice_fiscal_category_id.id
            fiscal_position = self._fiscal_position_map(
                result, False, partner_id=partner_id,
                partner_invoice_id=partner_id, company_id=company_id,
                fiscal_category_id=company.out_invoice_fiscal_category_id.id)

            result['value'].update(
                {'fiscal_position': fiscal_position['value']['fiscal_position']})

        return result

    @api.multi
    def _verify_company(self, vals):
        result = True
        msg_warning = ''
        sale_fields = {'partner_id': 'res.partner',
                       'warehouse_id': 'stock.warehouse'
                       }

        if 'company_id' in vals:
            company_id = vals['company_id']
        else:
            company_id = self.company_id.id

        for key, value in sale_fields.items():
            if key in vals:
                obj_SF = self.env[value].browse(vals[key])
            else:
                obj_SF = self[key]

            if obj_SF.company_id.id and obj_SF.company_id.id != company_id:
                result = False
                obj_comp = self.env['res.company'].browse(company_id)
                msg_warning += "\n" + \
                    (u"(%s, possuí empresa %s que é diferente de %s da cotação)"
                     % (obj_SF._description, obj_SF.company_id.name, obj_comp.name))

        if not result:
            raise Warning(
                u"Movimentação não permitida!",
                u"Em função do controle multiempresa, não é \
                 permitido salvar cotações com empresas diferentes %s"
                % (msg_warning))

        return result

    @api.multi
    def write(self, vals):
        if self._verify_company(vals):
            return super(SaleMulticompany, self).write(vals)

    @api.model
    def create(self, vals):
        if self._verify_company(vals):
            return super(SaleMulticompany, self).create(vals)
