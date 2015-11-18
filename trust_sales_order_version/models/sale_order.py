# -*- coding: utf-8 -*-
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


from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    version = fields.Char(u'Versão', size=4, default="A")

    def _increment_version(self):
        for inv in self:
            if inv.state != 'draft':
                version = inv.version or 'A'
                inv.version = chr(ord(version) + 1)

    @api.multi
    def action_quotation_send(self):
        self._increment_version()
        return super(SaleOrder, self).action_quotation_send()

    @api.multi
    def print_quotation(self):
        self._increment_version()
        return super(SaleOrder, self).print_quotation()
