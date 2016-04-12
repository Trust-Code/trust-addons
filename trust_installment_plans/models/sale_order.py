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

from datetime import datetime

from openerp import api, fields, models
from openerp.exceptions import Warning
from openerp.tools.translate import _


class PaymentInstallment(models.Model):
    _name = 'payment.installment'

    due_date = fields.Date(u'Data de vencimento')
    payment_mode_id = fields.Many2one('payment.mode',
                                      string=u"Forma de pagamento")
    amount = fields.Float(u'Total', digits=(18, 2))
    sale_order_id = fields.Many2one('sale.order',
                                    string=u"Pedido de Venda")

    account_invoice_id = fields.Many2one('account.invoice',
                                         string=u"Fatura")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('payment_installment_ids.amount')
    def _compute_difference(self):
        total = 0.0
        for item in self.payment_installment_ids:
            total += item.amount

        self.amount_difference = total - self.amount_total

    payment_installment_ids = fields.One2many('payment.installment',
                                              'sale_order_id',
                                              string=u"Parcelamento")

    amount_difference = fields.Float(u'Diferença', digits=(10, 2),
                                     readonly=True,
                                     compute='_compute_difference')

    @api.one
    @api.constrains('payment_installment_ids')
    def _check_amount_difference(self):
        if self.amount_difference != 0.0:
            raise Warning(_(u'Verifique as parcelas de pagamento,\
                            valor total difere das parcelas'))

    @api.one
    def generate_installment(self):
        if self.payment_term:
            values = self.payment_term.compute(self.amount_total)
            for item in self.payment_installment_ids:
                item.unlink()

            for item in values[0]:
                parcel = {'due_date': datetime.strptime(item[0], '%Y-%m-%d'),
                          'payment_mode_id': self.payment_mode_id.id,
                          'amount': item[1], 'sale_order_id': self.id}
                self.env['payment.installment'].create(parcel)

        else:
            Warning(_(u'Choose a payment term first'))

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        result = super(SaleOrder, self)._prepare_invoice(
            cr, uid, order, lines, context)

        installments = []
        for item in order.payment_installment_ids:
            installments.append(
                (0, False, {
                    'due_date': item.due_date, 'amount': item.amount}))
        result['payment_installment_ids'] = installments
        return result
