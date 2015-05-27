'''
Created on May 25, 2015

@author: danimar
'''

from openerp.osv import fields, osv


class res_partner(osv.Model):
    _inherit = 'res.partner'

    _columns = {
        'state_id': fields.many2one("res.country.state", 'State', ondelete='restrict', required=True),
    }

    _defaults = {
        'notify_email': lambda *args: 'none',
   }
