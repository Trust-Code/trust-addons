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

from openerp import api, models


class AccountTax(models.Model):
    """Implement computation method in taxes"""
    _inherit = 'account.tax'
    
    @api.v7
    def compute_all(self, cr, uid, taxes, price_unit, quantity,
                    product=None, partner=None, force_excluded=False,
                    fiscal_position=False, insurance_value=0.0,
                    freight_value=0.0, other_costs_value=0.0):
        #if fiscal_position:
        #    fiscal_position.asset_operation = True
        
        return super(AccountTax, self).compute_all(
            cr, uid, taxes, price_unit, quantity,
            product=product, partner=partner, force_excluded=force_excluded,
            fiscal_position=fiscal_position, insurance_value=insurance_value,
            freight_value=freight_value, other_costs_value=other_costs_value)
        
        
    @api.v8
    def compute_all(self, price_unit, quantity,
                    product=None, partner=None, force_excluded=False,
                    fiscal_position=False, insurance_value=0.0,
                    freight_value=0.0, other_costs_value=0.0):
            
        return self._model.compute_all(
            self._cr, self._uid, self, price_unit, quantity,
            product=product, partner=partner, force_excluded=force_excluded,
            fiscal_position=fiscal_position, insurance_value=insurance_value,
            freight_value=freight_value, other_costs_value=other_costs_value)
        