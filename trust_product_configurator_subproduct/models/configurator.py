# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductAttributeConfiguredProduct(models.Model):
    _inherit = 'sale.order.configured.product.attribute'

    for_subproduct = fields.Boolean("Usar para subprodutos")


class SaleOrderConfiguredProducts(models.Model):
    _inherit = 'sale.order.configured.product'

    sub_product_attributes = fields.One2many(
        comodel_name='sale.order.configured.product.attribute',
        inverse_name='product_line',
        string='Atributos de produto', copy=True,
        domain=[('for_subproduct', '=', True)],
        readonly=True, states={'draft': [('readonly', False)]})
