# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 TrustCode - www.trustcode.com.br                         #
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


{
    'name': 'Trustcode - Simples Nacional',
    'summary': """Módulo que facilita o cadastro de impostos e faixas de
        faturamento para o Simples Nacional""",
    'version': '8.0',
    'category': 'Localisation',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Danimar Ribeiro <danimaribeiro@gmail.com>',
                     'Mackilem Van der Laan Soares <mack.vdl@gmail.com>'
                     ],
    'depends': [
        'l10n_br_account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron_simples_nacional.xml',
        'views/res_company_view.xml',
    ],
    'instalable': True
}
