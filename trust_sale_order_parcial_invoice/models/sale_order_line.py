# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    quantity_to_invoice = fields.Float(string="Quantidade a Faturar")
