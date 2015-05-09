'''
Created on May 7, 2015

@author: danimar
'''

from openerp import models, api, fields

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'
    
    largura = fields.Float(string="Largura", digits=(16,6))
    comprimento = fields.Float(string="Comprimento", digits=(16,6))
    altura = fields.Float(string="Altura", digits=(16,6))
    