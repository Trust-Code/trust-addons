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


from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_installment_ids = fields.One2many('payment.installment',
                                              'account_invoice_id',
                                              string=u"Parcelamento")

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        result = super(
            AccountInvoice,
            self).finalize_invoice_move_lines(move_lines)
        index = 0
        if len(self.payment_installment_ids) > 0:
            for item in result:
                account = self.env['account.account'].browse(
                    item[2]['account_id'])
                if account and account.type == 'receivable':
                    item[2]['date_maturity'] = \
                        self.payment_installment_ids[index].due_date
                    item[2]['debit'] = self.payment_installment_ids[
                        index].amount
                    index += 1
        return result
