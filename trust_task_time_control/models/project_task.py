'''
Created on Nov 4, 2015

@author: developer
'''
from openerp import api, fields, models

class ProjectTask (models.Model):
    _inherit = 'project.task'
    
    @api.multi
    def write(self, vals):
        print vals
        if "stage_id" in vals:
            print self.stage_id 
            print vals["stage_id"]            
            stage = self.env['project.task.type'].browse(vals["stage_id"])
            #if stage.conta_tempo:
                                
                
                #pass
        return super(ProjectTask, self).write(vals)