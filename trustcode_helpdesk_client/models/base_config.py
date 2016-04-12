# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 Trustcode - www.trustcode.com.br                         #
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


class ResCompany(models.Model):
    _inherit = 'res.company'

    url_trustcode = fields.Char(u'Url Trustcode', size=100)


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    url_trustcode = fields.Char(u'Url Trustcode', size=100)

    def get_default_url_trustcode(
            self, cr, uid, fields, context=None):
        user = self.pool['res.users'].browse(cr, uid, uid, context)
        return {'url_trustcode':
                user.company_id.url_trustcode}

    @api.multi
    def set_cancel_url_trustcode(self):
        self.env.user.company_id.url_trustcode = \
            self.url_trustcode
