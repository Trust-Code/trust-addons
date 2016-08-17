# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def onchange_partner_id(self, partner_id, **kwargs):
        result = super(SaleOrder, self).onchange_partner_id(partner_id)
        partner = self.env['res.partner'].browse(partner_id)
        is_company = partner.is_company
        result['value']['is_company'] = is_company
        return result

    is_company = fields.Boolean(string="Echo")
