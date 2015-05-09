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

{
    'name': 'Second Unit of Measure',
    'summary': """In the industry segment is very important to control the stock of 
        a product with two unit of measures. """,
    'version': '8.0',
    'category': 'MRP',  
    'author': 'TrustCode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Danimar Ribeiro <danimaribeiro@gmail.com>',
                     'Mackilem Van der Laan Soares <mack.vdl@gmail.com>',
                     ],    
    'depends': [
            'product', 'sale', 'mrp'
    ],
    'data': [
        'views/product_template_view.xml',
        'views/res_config_view.xml',
        'views/sale_order_view.xml',
        'views/mrp_bom_view.xml',
        'security/second_unit_security.xml',
    ],    
    'application':True,    
}
