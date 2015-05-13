# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU General Public License for more details.                                 #
#                                                                             #
#You should have received a copy of the GNU General Public License            #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _

class sale_product_configurator(orm.Model):
    _inherit = 'sale.order'
    
    _columns = {
            'resin': fields.selection([
                                      ('isophthalic','Isophthalic'),
                                      ('off-shore','Off-Shore'),
                                      ('orthophthalic','Orthophthalic'), 
                                      ('phynolic','Phynolic'),
                                      ('vinyl ester','Vinyl Ester')],
                                      'Resin', readonly=False, select=True, required=True),
            'fixation': fields.selection([
                                          ('stainless steel 304','Stainless Steel 304'),
                                          ('stainless steel 316','Stainless Steel 316'),
                                          ('stainless steel 316L','Stainless Steel 316L'),
                                          ],'Fixation', readonly=False, select=True, required=True),
            'color': fields.selection([
                                      ('yellow safety','Yellow Safety'),
                                      ('gray','Gray'),
                                      ('yellow safety/gray','Yellow Safety/Gray'),
                                      ('green','Green'),
                                      ('write','Write'),
                                      ('special','Special'),
                                      ],'Color', readonly=False, select=True, required=True),
            'special color': fields.char ('Special Color', size=20, help='Insert here the special color.'),
                }
    
    _defaults = {
                 'resin': 'isophthalic',
                 'fixation': 'stainless steel 304',
                 'color': 'yellow safety/gray',
                 }



