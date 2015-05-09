# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Danimar Ribeiro - www.trustcode.com.br                   #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU General Public License for more details.                                 #
#                                                                             #
#You should have received a copy of the GNopp_idU General Public License            #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################

from openerp import models, api, fields

class calendar_event_followup(models.Model):
    _inherit='calendar.event'
    
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    related_to_sales = fields.Boolean(string="Sales Related?")

class crm_phonecall_followup(models.Model):
    _inherit='crm.phonecall'
    
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")


class sale_order_followup(models.Model):
    _inherit = 'sale.order'
    
    def _meeting_count(self):
        self.meeting_count = self.env['calendar.event'].search_count([('sale_order_id', '=', self.id)])
                    
    meeting_count=fields.Integer(compute='_meeting_count', string='# Meetings')
    
    @api.multi
    def action_create_meeting(self):
        """
        Open meeting's calendar view to schedule meeting on current opportunity.
        :return dict: dictionary value for created Meeting view
        """
        res = self.env['ir.actions.act_window'].for_xml_id('calendar', 'action_calendar_event')
        partner_ids = [self.env.user.partner_id.id]
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        res['context'] = {            
            'default_partner_id': self.partner_id and self.partner_id.id or False,
            'default_partner_ids': partner_ids,
            'default_sale_order_id': self.id,
            'default_related_to_sales': True,
        }
        return res
    
    