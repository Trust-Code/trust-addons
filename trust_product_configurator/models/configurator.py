# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError


class ProductAttributeConfiguredProduct(models.Model):
    _name = 'sale.order.configured.product.attribute'

    @api.one
    @api.depends('attribute', 'product_line.product_tmpl_id',
                 'product_line.product_tmpl_id.attribute_line_ids')
    def _get_possible_attribute_values(self):
        attr_values = self.env['product.attribute.value']
        for attr_line in self.product_line.product_tmpl_id.attribute_line_ids:
            if attr_line.attribute_id.id == self.attribute.id:
                attr_values |= attr_line.value_ids
        self.possible_values = attr_values.sorted()

    product_line = fields.Many2one(
        comodel_name='sale.order.configured.product',
        string='Produto Configurado')
    attribute = fields.Many2one(
        comodel_name='product.attribute', string='Atributo')
    attr_type = fields.Selection(string='Tipo', store=False,
                                 related='attribute.attr_type')
    numeric_value = fields.Float('Valor Numérico', digits=(12, 6))
    value = fields.Many2one(
        comodel_name='product.attribute.value', string='Valor',
        domain="[('id', 'in', possible_values[0][2])]")
    possible_values = fields.Many2many(
        comodel_name='product.attribute.value', string="Valores possíveis",
        compute='_get_possible_attribute_values', readonly=True)


class SaleOrderConfiguredProducts(models.Model):
    _name = 'sale.order.configured.product'
    _description = 'Produtos configurados no pedido de venda'

    # Prova de conceito - adicionar campo dinâmico na tela
    # funciona bem e o campo é enviado ao write
    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False,
                        submenu=False):
        res = super(SaleOrderConfiguredProducts, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            eview = etree.fromstring(res['arch'])
            summary = eview.xpath("//field[@name='quantity']")
            if len(summary):
                summary = summary[0]
                summary.addnext(etree.Element('field', {'name': 'teste',
                                                        'string': 'Teste',
                                                        }))
                print res
                res['fields']['teste'] = {
                    'change_default': False, 'string': 'Teste',
                    'searchable': True, 'views': {}, 'required': False,
                    'manual': False, 'readonly': True,
                    'depends': [], 'company_dependent': False,
                    'sortable': True, 'type': 'integer', 'store': True
                }
            res['arch'] = etree.tostring(eview)

        return res

    @api.multi
    def name_get(self):
        return [(rec.id, rec.product_tmpl_id.name) for rec in self]

    state = fields.Selection([('draft', 'Provisório'), ('done', 'Confirmado')],
                             string="Status", default='draft')
    sale_order_id = fields.Many2one('sale.order', string='Pedido de venda',
                                    readonly=True)
    order_line_id = fields.Many2one('sale.order.line',
                                    string="Linha do pedido relacionada",
                                    readonly=True)

    product_tmpl_id = fields.Many2one(
        'product.template', string="Template de produto",
        domain="[('configurator_template', '=', True)]",
        readonly=True, states={'draft': [('readonly', False)]})
    quantity = fields.Integer(
        string="Quantidade", readonly=True,
        states={'draft': [('readonly', False)]})

    product_attributes = fields.One2many(
        comodel_name='sale.order.configured.product.attribute',
        inverse_name='product_line',
        string='Atributos de produto', copy=True,
        readonly=True, states={'draft': [('readonly', False)]})

    @api.multi
    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        self.ensure_one()
        self.product_attributes = (
            [(2, x.id) for x in self.product_attributes] +
            [(0, 0, x) for x in
             self.product_tmpl_id._get_product_attributes_dict()])

    def _check_line_confirmability(self):
        if any(not bool(line.value) for line in self.product_attributes):
            raise UserError(
                _("Você não pode confirmar antes de selecionar os atributos."))

    @api.multi
    def confirm_done(self):
        self.ensure_one()
        product_obj = self.env['product.product']
        sale_line_obj = self.env['sale.order.line']
        if self.product_tmpl_id:
            self._check_line_confirmability()
            if self.order_line_id:
                self.order_line_id.product_id.unlink()
                self.order_line_id.unlink()

            attr_values = self.product_attributes.mapped('value')
            # Filter the product with the exact number of attributes values
            product = product_obj.create(
                {'product_tmpl_id': self.product_tmpl_id.id,
                 'attribute_value_ids': [(6, 0, attr_values.ids)]})

            sale_line = sale_line_obj.create({
                'product_id': product.id, 'product_uom_qty': self.quantity,
                'price_unit': product.list_price,
                'order_id': self.sale_order_id.id,
            })
            self.write({'order_line_id': sale_line.id, 'state': 'done'})
