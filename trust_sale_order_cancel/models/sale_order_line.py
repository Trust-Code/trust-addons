# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, models
from openerp.exceptions import Warning as UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def call_cancel_wizard(self):
        if self.state == 'done' or self.state == 'cancel':
            raise UserError(
                'Movimentação Proibida!',
                'Esta linha do pedido já foi cancelada ou concluída!')

        return({
            'name': 'Cancelar Produtos Parcialmente',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line.cancel',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_line_id': self.id,
                        'default_invoice_amount': self.product_uom_qty}
        })
