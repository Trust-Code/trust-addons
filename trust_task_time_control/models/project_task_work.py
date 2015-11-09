'''
Created on Nov 5, 2015

@author: developer
'''
from openerp import api, fields, models


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    time_open = fields.Boolean('Time Open')