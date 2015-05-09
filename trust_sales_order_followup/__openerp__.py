# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Danimar Ribeiro - www.trustcode.com.br                   #
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
    'name': 'Sales Order Follow-Up',
    'summary': "Add follow-up capabilities to sales order like in the leads",
    'version': '1.0',
    'category': 'Sales',  
    'author': 'TrustCode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Danimar Ribeiro <danimaribeiro@gmail.com>',
                     'Mackilem Van der Laan Soares <mack.vdl@gmail.com>'],
    'description': """
          This module allows to register phone-calls, schedule them for a specific sales order
          or for a customer.
    """,
    'depends': [
        'crm',
        'sale'
    ],
    'data': [
        'views/sales_order_followup.xml',
    ],
    'installable': True,
    'application':True,
    'active': False,
}
