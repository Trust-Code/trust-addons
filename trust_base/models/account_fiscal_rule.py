'''
Created on May 24, 2015

@author: danimar
'''

from openerp import fields, api, models
from openerp.osv import osv


class account_fiscal_rule(models.Model):
    _inherit = 'account.fiscal.position.rule'    
    
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position',
        domain="[('company_id','=',company_id)]", select=True, required=True)
    

