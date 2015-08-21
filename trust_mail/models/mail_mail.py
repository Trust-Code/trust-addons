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


from openerp import models, api


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False,
             raise_exception=False, context=None):
        ir_mail_server = self.env['ir.mail_server']
        res_users = self.env['res.users']
        for email in self:
            user = res_users.search([('partner_id', '=', email.author_id.id)])
            if user:
                server_id = ir_mail_server.search(
                    [('smtp_user', '=', user.email)])
                server_id = server_id and server_id[0] or False
                if server_id:
                    email.mail_server_id = server_id.id
                    email.reply_to = email.email_from
        return super(MailMail, self).send(auto_commit=auto_commit,
                                          raise_exception=raise_exception,
                                          context=context)
