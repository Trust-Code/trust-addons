# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
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

import base64
from lxml import etree
from openerp import api, fields, models


class BaseNfse(models.Model):
    _inherit = 'base.nfse'
    
    
    @api.multi
    def send_rps(self):
        if self.city_code == '6291': # Campinas
            pass #TODO Implementar envio       
        
        return super(BaseNfse, self).send_rps()
        
    
    @api.multi
    def cancel_nfse(self):
        if self.city_code == '6291': # Campinas
            pass #TODO Implementar envio       
        
        return super(BaseNfse, self).cancel_nfse()
        
                
        
    @api.multi
    def check_nfse_by_rps(self):
        if self.city_code == '6291': # Campinas
            pass #TODO Implementar envio       
        
        return super(BaseNfse, self).check_nfse_by_rps()
        
    
    @api.multi
    def check_nfse_by_lote(self):
        if self.city_code == '6291': # Campinas
            pass #TODO Implementar envio       
        
        return super(BaseNfse, self).check_nfse_by_lote()
        
    
    @api.multi
    def generate_pdf(self):
        if self.city_code == '6291': # Campinas
            pass #TODO Implementar envio       
        
        return super(BaseNfse, self).generate_pdf()
        
    
    
    