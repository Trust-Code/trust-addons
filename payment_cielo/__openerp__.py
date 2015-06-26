# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-Trust-Code (<http://www.trustcode.com.br>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Cielo Checkout Payment Acquirer',
    'category': 'Hidden',
    'summary': 'Payment Acquirer: Cielo Checkout Implementation',
    'version': '1.0',
    'description': """Cielo Checkout Payment Acquirer""",
    'author': 'TrustCode',
    'depends': ['payment'],
    'data': [
        'views/cielo.xml',
        'views/payment_acquirer.xml',
        'views/res_config_view.xml',
        'data/cielo.xml',
    ],
    'installable': True,
}
