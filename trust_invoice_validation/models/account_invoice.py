# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
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


from openerp import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _invoice_rules_validate(self):
        rules = self.env['account.invoice.rules'].search(
            [('use_in', '=', 'account.invoice')])
        rules.validate(self)
        rules = self.env['account.invoice.rules'].search(
            [('use_in', '=', 'account.invoice.line')])
        if rules:
            for line in self.invoice_line:
                rules.validate(self, line)

    @api.multi
    def nfe_check(self):
        result = super(AccountInvoice, self).nfe_check()
        self._invoice_rules_validate()
        return result

    @api.multi
    def validate_nfse(self):
        result = super(AccountInvoice, self).validate_nfse()
        self._invoice_rules_validate()
        return result
