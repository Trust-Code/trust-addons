'''
Created on Nov 4, 2015

@author: developer
'''
from openerp import api, fields, models

class HrAttendance (models.Model):
    _inherit = 'hr.employee'
    
    @api.multi
    def attendance_action_change(self):
        print 'chamou'
        return super(HrAttendance, self).attendance_action_change()