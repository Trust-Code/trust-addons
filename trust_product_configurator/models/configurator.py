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
    value_str = fields.Char("Valor Selecionado", size=40)
    possible_values = fields.Many2many(
        comodel_name='product.attribute.value', string="Valores possíveis",
        compute='_get_possible_attribute_values', readonly=True)

    @api.multi
    def write(self, vals):
        if 'numeric_value' in vals:
            vals['value_str'] = vals['numeric_value']
        if 'value' in vals:
            value = self.env['product.attribute.value'].browse(vals['value'])
            vals['value_str'] = value.name
        return super(ProductAttributeConfiguredProduct, self).write(vals)


class ProductConfiguratorBomLine(models.Model):
    _name = 'product.configurator.bom.line'

    product_line = fields.Many2one(
        comodel_name='sale.order.configured.product',
        string='Produto Configurado')

    bom_line_id = fields.Many2one('mrp.bom.line', string='Linha BOM')
    product_template_id = fields.Many2one(
        string='Subproduto', store=False,
        related='bom_line_id.product_template')
    quantity = fields.Float(related="bom_line_id.product_qty",
                            string="Quantidade")
    configured = fields.Boolean(string="Configurado", default=False)

    @api.multi
    def open_wizard_configure(self):
        print "ok"
        pass


class ProductConfiguratorWizard(models.TransientModel):
    _name = 'product.configurator.wizard'

    sale_product_id = fields.Many2one('sale.order.configured.product',
                                      string="Produto Configurado")
    product_id = fields.Many2one(related='sale_product_id.product_tmpl_id')

    @api.multi
    def write(self, vals):
        for key, value in vals.iteritems():
            if key.startswith('dynamic_'):
                id_attr = int(key.replace('dynamic_', ''))
                prod_attribute = self.sale_product_id.product_attributes.\
                    filtered(lambda x: x.attribute.id == id_attr)
                if isinstance(value, basestring):
                    value_id = int(value.replace('value_', ''))
                    prod_attribute.value = value_id
                else:
                    prod_attribute.numeric_value = value

        super(ProductConfiguratorWizard, self).write(vals)
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        result = super(ProductConfiguratorWizard, self).read(fields, load)
        for res in result:
            current_id = self.browse(res['id'])
            if current_id:
                for prod_attr in current_id.sale_product_id.product_attributes:
                    attr_name = 'dynamic_%s' % prod_attr.attribute.id
                    if prod_attr.attribute.attr_type == 'selection':
                        if prod_attr.value.id:
                            res[attr_name] = 'value_%s' % prod_attr.value.id
                    else:
                        res[attr_name] = prod_attr.numeric_value
        return result

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False,
                        submenu=False):
        res = super(ProductConfiguratorWizard, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            eview = etree.fromstring(res['arch'])
            sale_product_id = eview.xpath("//field[@name='sale_product_id']")
            if len(sale_product_id) and "current_id" in self.env.context:
                sale_product_id = sale_product_id[0]

                current_id = self.browse(
                    self.env.context['current_id'])
                add_attributes = []
                for attribute in current_id.product_id.attribute_line_ids:
                    values = []
                    for value in attribute.value_ids:
                        values.append({
                            'id': 'value_%s' % value.id,
                            'name': value.name,
                        })

                    add_attributes.append({
                        'name': 'dynamic_%s' % attribute.attribute_id.id,
                        'string': attribute.attribute_id.name,
                        'type': attribute.attribute_id.attr_type,
                        'required': attribute.required,
                        'values': values,
                    })

                for add_attr in add_attributes:
                    sale_product_id.addnext(etree.Element(
                        'field', {'name': add_attr['name'],
                                  'string': add_attr['string'],
                                  'modifiers': '{ "required": true }'}
                        ))
                    vals = {
                        'string': add_attr['string'],
                        'required': add_attr['required'],
                        'type': add_attr['type'],
                    }
                    selection = []
                    if add_attr['type'] == 'selection':
                        for value in add_attr['values']:
                            selection.append(
                                [value['id'], value['name']]
                            )
                        vals['selection'] = selection

                    res['fields'][add_attr['name']] = vals

            res['arch'] = etree.tostring(eview)
        return res


class SaleOrderConfiguredProducts(models.Model):
    _name = 'sale.order.configured.product'
    _description = 'Produtos configurados no pedido de venda'

    @api.multi
    def open_wizard_configure(self):
        mod_obj = self.env['ir.model.data']
        result = mod_obj.get_object_reference(
            'trust_product_configurator',
            'view_product_configurator_wizard_form')
        wiz_id = self.env['product.configurator.wizard'].create({
            'sale_product_id': self.id,
        })
        return {
            'name': 'Configurar produto',
            'type': 'ir.actions.act_window',
            'res_model': 'product.configurator.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz_id.id,
            'views': [(result[1], 'form')],
            'target': 'new',
            'context': {'current_id': wiz_id.id},
            'flags': {'form': {'action_buttons': True, 'options':
                               {'mode': 'edit'}}},
        }

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
        string="Quantidade", readonly=True, default=1.0,
        states={'draft': [('readonly', False)]})

    product_attributes = fields.One2many(
        comodel_name='sale.order.configured.product.attribute',
        inverse_name='product_line',
        string='Atributos de produto', copy=True,
        readonly=True, states={'draft': [('readonly', False)]})

    bom_line_ids = fields.One2many(
        comodel_name='product.configurator.bom.line',
        inverse_name='product_line',
        string='Subprodutos', copy=True,
        readonly=True, states={'draft': [('readonly', False)]}
    )

    @api.multi
    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        self.ensure_one()
        self.product_attributes = (
            [(2, x.id) for x in self.product_attributes] +
            [(0, 0, x) for x in
             self.product_tmpl_id._get_product_attributes_dict()])

        if self.product_tmpl_id:
            bom = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', self.product_tmpl_id.id)], limit=1)

            lines = []
            for bom_line in bom.bom_line_ids:
                lines.append((0, 0, {
                    'product_line': self.id,
                    'bom_line_id': bom_line.id,
                }))
            self.bom_line_ids = (
                lines
            )

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
