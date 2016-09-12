# -*- coding: utf-8 -*-
# © 2015 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    largura = fields.Float(string="Largura", digits=(16, 6))
    comprimento = fields.Float(string="Comprimento", digits=(16, 6))
    altura = fields.Float(string="Altura", digits=(16, 6))
