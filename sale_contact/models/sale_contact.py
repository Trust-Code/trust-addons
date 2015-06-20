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

from openerp.osv import orm, fields

class SaleContact(orm.Model):
    _inherit = 'sale.order'
    
    _columns = {
              'partner_contact_id': fields.many2one('res.partner', 
                                                     'partner_id',
                                                     domain="[('parent_id','=',partner_id)]",
                                                     readonly=True,
                                                     required=True,
                                                     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                                     help="Insert here the comercial contact."),
                }
