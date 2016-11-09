# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    @api.depends('debit', 'credit', 'payment_type', 'maturity_residual')
    def _compute_amounts(self):
        for item in self:
            amount = item.debit if item.payment_type == 'receivable' \
                else item.credit
            item.amount_to_pay = amount
            item.amount_paid = abs(item.amount_to_pay) - abs(item.maturity_residual)
            if item.payment_type == 'payable':
                item.amount_paid *= -1

    amount_to_pay = fields.Float(string="A Pagar/Receber",
                                 compute="_compute_amounts")
    amount_paid = fields.Float(string="Pago/Recebido",
                               compute="_compute_amounts")

    payment_type = fields.Selection(
        string="Tipo",
        related="account_id.type"
    )

    @api.multi
    def action_redirect_to_payment(self):
        self.ensure_one()
        if self.payment_type == 'receivable':
            dummy, action_id = self.env['ir.model.data'].get_object_reference(
                'account_voucher', 'action_vendor_receipt')
            context = "{'type':'receipt', 'default_partner_id': %s, \
                'default_amount': %d}" % (self.partner_id.id,
                                          self.maturity_residual)
        else:
            dummy, action_id = self.env['ir.model.data'].get_object_reference(
                'account_voucher', 'action_vendor_payment')
            context = "{'type':'payment', 'default_partner_id': %s, \
                'default_amount': %d}" % (self.partner_id.id,
                                          self.maturity_residual*-1)
        vals = self.env['ir.actions.act_window'].browse(action_id).read()[0]
        vals['context'] = context
        vals['views'] = [vals['views'][1], vals['views'][0]]
        return vals
