'''
Created on May 24, 2015

@author: danimar
'''

from openerp import fields, api, models
from openerp.osv import osv


class sale_order(models.Model):
    _inherit = 'sale.order'    
    
    fiscal_position = fields.Many2one('account.fiscal.position', string='Fiscal Position',
                 required=True, domain="[('fiscal_category_id', '=', fiscal_category_id)]",
                 readonly=True, states={'draft': [('readonly', False)]})
    
    delivery_after = fields.Integer(string='Prazo de entrega (dias)', default=30)

