'''
Created on 2 de set de 2015

@author: danimar
'''

from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_installment_ids = fields.One2many('payment.installment',
                                          'account_invoice_id',
                                          string=u"Parcelamento")

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        result = super(AccountInvoice, self).finalize_invoice_move_lines(move_lines)
        index = 0
        for item in result:
            account = self.env['account.account'].browse(item[2]['account_id'])
            if account and account.type == 'receivable':                
                item[2]['date_maturity'] = self.payment_installment_ids[index].due_date
                item[2]['debit'] = self.payment_installment_ids[index].amount
                index += 1    
        return result
        