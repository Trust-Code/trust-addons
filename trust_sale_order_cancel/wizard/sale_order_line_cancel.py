# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class SaleOrderLineCancel(models.TransientModel):
    _name = 'sale.order.line.cancel'

    cancel_amount = fields.Float(string='Quantidade a Cancelar')
    sale_order_line_id = fields.Many2one('sale.order.line',
                                         string="Produtos")
    invoice_amount = fields.Float(string="Quantidade de Pedido", readonly=1)

    @api.onchange("cancel_amount")
    def _onchange_cancel_amount_trust_sale_order_cancel(self):
        vals = {}

        if self.cancel_amount > self.sale_order_line_id.product_uom_qty:
            vals['warning'] = {
                'title': 'Ação Não Permitida',
                'message': 'Você está tentando cancelar mais itens que o \
pedido original'
            }

        return vals

    @api.multi
    def cancel_sale_order_line(self):
        amount = self.sale_order_line_id.product_uom_qty
        to_cancel = self.cancel_amount
        to_invoice = amount - to_cancel

        if self.cancel_amount <= 0:
            raise UserError(
                'Movimentação não permitida!',
                'Você está tentando cancelar uma quantidade menor ou igual \
                zero produtos.')

        if to_cancel < amount:
            # Cancelando aquisição e linha do pedido
            proc_order = self.env['procurement.order'].search(
                [('sale_line_id', '=', self.sale_order_line_id.id)])

            self.sale_order_line_id.write({'state': 'cancel'})

            new_order_line = self.sale_order_line_id.copy({
                'product_uom_qty': to_invoice, 'state': 'confirmed',
                'order_id': self.sale_order_line_id.order_id.id})

            new = proc_order.copy({'product_qty': to_invoice,
                                   'sale_line_id': new_order_line.id})
            proc_order.write({'product_uom_qty': to_cancel})
            proc_order.cancel()
            new.run()

        elif to_cancel > amount:
            raise UserError(
                'Movimentação Bloqueada!',
                'Quantidade a cancelar é maior que a original do pedido.')

        elif to_cancel == amount:
            # Cancelando aquisição e linha do pedido
            proc_order = self.env['procurement.order'].search(
                [('sale_line_id', '=', self.sale_order_line_id.id)])
            proc_order.cancel()
            self.sale_order_line_id.write({'state': 'cancel'})

        lines = self.sale_order_line_id.order_id.order_line
        remaining = len(lines.filtered(lambda x: x.state != 'cancel'))
        if remaining == 0:  # Cancelar pedido se todos os itens cancelaram
            self.sale_order_line_id.order_id.action_cancel()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            }
