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
            if item.state != 'done' and item.state != 'cancel':
                lista.append((0, 0, {'sale_order_line_id': item.id,
                                     'name': item.name,
                                     'quantidade': item.product_uom_qty,
                                     'subtotal': item.price_subtotal}))

        vals = {"sale_order_line_id": lista}

        return {"value": vals}

    @api.multi
    def faturar_parcial(self):
        lines = self.sale_order_line_id
        order_lines = self.env['sale.order.line'].browse(0)
        for line in lines:
            if line.a_faturar and line.a_faturar > 0 and\
                    line.a_faturar < line.quantidade and\
                    line.sale_order_line_id.state != 'done' and\
                    line.sale_order_line_id.state != 'cancel':
                sale_order_line = self.env['sale.order.line'].\
                    browse(line.sale_order_line_id.id)
                to_invoice = line.a_faturar
                remain = line.quantidade - to_invoice
                new_line = sale_order_line.copy({'product_uom_qty': to_invoice,
                                                 'state': 'done', })
                sale_order_line.write({'product_uom_qty': remain})
                order_lines += new_line
                # self.env.cr.commit()
            else:
                raise UserError(
                    'Movimentação Não Permitida',
                    'A quantia à faturar deve ser menor que a quantia do pedido e \
maior que zero.')
        if order_lines:
            order = new_line[0].order_id
            invoice_line_ids = order_lines.invoice_line_create()
            self.env['sale.order']._make_invoice(order,
                                                 invoice_line_ids)
