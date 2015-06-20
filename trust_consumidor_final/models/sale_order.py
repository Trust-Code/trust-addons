# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
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

from openerp import fields, api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'  
    
    ind_final = fields.Selection([
            ('0', u'Não'),
            ('1', u'Consumidor final')], 
            string=u'Operação com Consumidor final', required=False,
            help=u'Indica operação com Consumidor final.', default='0')
    
    @api.multi
    def onchange_partner_id(self, partner_id, **kwargs):
        result = super(SaleOrder, self).onchange_partner_id(partner_id)
        partner = self.env['res.partner'].browse(partner_id)
        ind_final = partner.ind_final
        if not ind_final:
            ind_final = '0' if partner.is_company else '1'
        result['value']['ind_final'] = ind_final      
        return result
    
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        result = super(SaleOrder, self)._prepare_invoice(
            cr, uid, order, lines, context)
        
        result['ind_final'] = order.ind_final
        return result
