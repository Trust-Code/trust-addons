'''
Created on Nov 5, 2015

@author: developer
'''
from openerp import api, fields, models
from openerp.osv import fields, osv

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    _columns = {
        'count_time': fields.boolean('Count Time'),
        #'active': fields.Boolean('Active'),
        }