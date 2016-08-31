# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    sale_order_line_id = fields.One2many(
        comodel_name='sale.advance.payment.inv.line', string="Produtos",
        inverse_name="sale_advance_ref")

    def onchange_method(self, cr, uid, ids, advance_payment_method, product_id,
                        context=None):
        sale_order = self.pool.get('sale.order').browse(
            cr, uid, context['active_id'], context)
        sale_order_line = sale_order.order_line
        lista = []

        for item in sale_order_line:
            if item.state != 'done' and item.state != 'cancel'\
                    and item.product_uom_qty > 0:
                lista.append((0, 0, {'sale_order_line_id': item.id,
                                     'name': item.name,
                                     'quantidade': item.product_uom_qty,
                                     'subtotal': item.price_subtotal}))

        vals = {"sale_order_line_id": lista}

        return {"value": vals}

    @api.multi
    def faturar_parcial(self):
        error_message = ''
        lines = self.sale_order_line_id
        order_lines = self.env['sale.order.line'].browse(0)
        for line in lines:
            if line.a_faturar:
                if line.a_faturar < 0:
                    message = "Você não pode faturar uma quantidade menor que \
zero.\n"
                    error_message += message
                if line.a_faturar > line.quantidade:
                    message = "Você não pode faturar uma quantidade maior que \
a do pedido.\n"
                    error_message += message
                if line.sale_order_line_id.state == 'done':
                    message = "Você está tentando faturar uma linha que já \
está concluída.\n"
                    error_message += message
                if line.sale_order_line_id.state == 'cancel':
                    message = "Você está tentando faturar uma linha que já foi \
cancelada\n"
                    error_message += message

            if line.a_faturar == 0:
                message = "Você não pode faturar zero produtos.\n"
                error_message += message

            if len(error_message) == 0:
                sale_order_line = self.env['sale.order.line'].\
                    browse(line.sale_order_line_id.id)
                to_invoice = line.a_faturar
                remain = line.quantidade - to_invoice
                if remain != 0:
                    new_line = sale_order_line.copy(
                        {'product_uom_qty': to_invoice,
                         'state': 'done', })
                    sale_order_line.write({'product_uom_qty': remain})
                else:
                    new_line = line.sale_order_line_id
                    new_line.write({'state': 'done'})
                order_lines += new_line

            else:
                raise UserError(
                    'Movimentação Não Permitida',
                    error_message)
        if order_lines:
            order = new_line[0].order_id
            invoice_line_ids = order_lines.invoice_line_create()
            self.env['sale.order']._make_invoice(order,
                                                 invoice_line_ids)
