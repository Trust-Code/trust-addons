# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_view_parcial_invoice(self):
        invoice_ids = []
        invoices = self.env['account.invoice'].search(
            [('origin', '=', self.name)])
        for i in invoices:
            invoice_ids.append(i.id)

        return({
            'name': u'Faturas Provisórias de %s' % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', invoice_ids)]
            })
