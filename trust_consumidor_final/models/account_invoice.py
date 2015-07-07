'''
Created on 06/07/2015

@author: danimar
'''

from openerp import models, api

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity',
                 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id', 'fiscal_position')
    def _compute_price(self):
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = self.invoice_line_tax_id.compute_all(
            price, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id,
            fiscal_position=self.fiscal_position, consumidor=self.invoice_id.ind_final)
        self.price_subtotal = taxes['total'] - taxes['total_tax_discount']
        self.price_total = taxes['total']
        if self.invoice_id:
            self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)
            self.price_total = self.invoice_id.currency_id.round(self.price_total)