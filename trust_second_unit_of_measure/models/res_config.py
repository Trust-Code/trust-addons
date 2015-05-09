'''
Created on May 7, 2015

@author: danimar
'''
from openerp import models, fields, api

class sale_configuration(models.Model):
    _inherit = 'sale.config.settings'
    
    group_second_uom =fields.Boolean(string="Allow using second unit of measure",
            implied_group='trust_second_unit_of_measure.group_second_uom',
            help="""Allows you to select and maintain the second unit of measure for products.""",
            default=False)
    