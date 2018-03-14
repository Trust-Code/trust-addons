# coding=utf-8
'''
Created on 2 de set de 2015

@author: danimar
'''

from openerp import models, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def print_quotation(self):
        super(SaleOrder, self).print_quotation()
        return self.env['report'].get_action(
            self, 'trust_sale_report_machado.report_sale')
