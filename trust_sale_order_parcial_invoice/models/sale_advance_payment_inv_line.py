# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class SaleAdvancePaymentInvLine(models.TransientModel):
    _name = "sale.advance.payment.inv.line"

    sale_order_line_id = fields.Many2one('sale.order.line', string="Produtos")
    name = fields.Char(string="Nome", readonly=True)
    quantidade = fields.Float(string="Quantidade", readonly=True)
    subtotal = fields.Float(string="Subtotal", readonly=True)
    a_faturar = fields.Float(string="A Faturar")
    sale_advance_ref = fields.Many2one('sale.advance.payment.inv')

    @api.onchange("sale_order_line_id")
    def _onchange_sale_order_line_id_trust_parcial_invoice(self):
        vals = {}
        produto = self.env['sale.order.line'].browse(self.sale_order_line_id)

        vals = {
            "name": produto.name,
            "quantidade": produto.product_uom_qty,
            "subtotal": produto.price_subtotal,
        }

        return vals
