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


import re
from openerp import api, fields, models
from openerp.models import NewId


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.depends('name')
    def _get_nfe_folders(self):
        name = 'empresa'
        idCompany = 0
        if not isinstance(self.id, NewId):
            idCompany = self.id
        if self.name:
            name = self.name.lower()
        name = re.sub('[^a-z0-9_]', '_', name)
        name = name[:20] + '_' + str(idCompany)
        self.nfe_export_folder = '/opt/xml/exp/' + name
        self.nfe_import_folder = '/opt/xml/imp/' + name
        self.nfe_backup_folder = '/opt/xml/bkp/' + name

    nfe_version = fields.Selection(
        [('1.10', '1.10'), ('2.00', '2.00'), ('3.10', '3.10')],
        string=u'Versão NFe', required=True, default="3.10", readonly=True)

    nfe_import_folder = fields.Char('Pasta de Importação', size=254,
                                    compute='_get_nfe_folders', readonly=True)
    nfe_export_folder = fields.Char('Pasta de Exportação', size=254,
                                    compute='_get_nfe_folders', readonly=True)
    nfe_backup_folder = fields.Char('Pasta de Backup', size=254,
                                    compute='_get_nfe_folders', readonly=True)
