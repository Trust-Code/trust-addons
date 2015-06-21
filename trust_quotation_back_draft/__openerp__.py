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

{
    'name': 'Button Back to Draft (Sent to Draft)',
    'description': """Insere botão para tornar possível retornar de enviado
                    para provisório""",
    'category': 'Sales',
    'license': 'AGPL-3',
    'author': 'Trust-Code',
    'website': 'www.trustcode.com.br',
    'contributors': ['Mackilem Van der Laan Soares <mack.vdl@gmail.com>',
                     'Danimar Ribeiro <danimaribeiro@gmail.com>'
                     ],
    'version': '8.0',
    'depends': ['sale'],
    'data': ['views/sale_order_view.xml', 'views/sale_workflow.xml'],
    'installable': True,
    'active': False,
}
