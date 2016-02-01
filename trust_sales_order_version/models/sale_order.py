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

    version = fields.Char(u'Versão', size=4, compute='_compute_version')

    @api.multi
    def _compute_version(self):
        obj_attach = self.env['ir.attachment'].search(
            [('res_id', '=', self.id)], 
            order='id desc', limit=1)

        self.version = obj_attach.res_version


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    res_version = fields.Char(u'Versão', size=4)


    @api.model
    def create(self, values):        
        if 'res_model' in values and values['res_model'] == 'sale.order':
            obj_so = self.env['sale.order'].browse(values['res_id'])
            get_version = obj_so.version
    
            if get_version:
                values.update({'res_version': chr(ord(get_version) + 1)})
            else:
                values.update({'res_version': 'A'})

        return super(IrAttachment, self).create(values)
'''