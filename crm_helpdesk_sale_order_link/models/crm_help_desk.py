# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class CrmHelpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    @api.multi
    def action_help2quotation(self):
        action = self.env['ir.model.data'].get_object('sale',
                                                      'action_quotations')
        view_ref = self.env['ir.model.data'].get_object(
            'sale', 'view_order_form'
            )
        return{
            'id': action.id,
            'name': action.name,
            'view_type': action.view_type,
            'view_mode': 'form',
            'res_model': action.res_model,
            'type': action.type,
            'view_id': view_ref.id,
            'search_view_id': action.search_view_id.id,
            'domain': action.domain,
            'context': action.context,
        }
