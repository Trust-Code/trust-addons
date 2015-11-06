'''
Created on Nov 5, 2015

@author: developer
'''
from openerp import api, fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    count_time = fields.Boolean('Count Time')