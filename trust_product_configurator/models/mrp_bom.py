# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.tools.safe_eval import safe_eval
from openerp.exceptions import Warning as UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def _bom_find(self, product_tmpl_id=None, product_id=None,
                  properties=None):
        domain = []
        if product_id:
            domain += [('product_id', '=', product_id)]
        if product_tmpl_id and not product_id:
            domain += [('product_id', '=', False),
                       ('product_tmpl_id', '=', product_tmpl_id)]
        if self.env.context.get('company_id', False):
            domain += [('company_id', '=', self.env.context['company_id'])]

        return self.env['mrp.bom'].search(domain, limit=1,
                                          order='sequence, product_id').id

    def _bom_search(self, product=None, template=None):
        if product:
            return self.env['mrp.bom'].search(
                [('product_id', '=', product.id)], limit=1)
        if template:
            return self.env['mrp.bom'].search(
                [('product_id', '=', False),
                 ('product_tmpl_id', '=', template.id)], limit=1)

    def _compute_bom_line(self, bom_line, product, attributes):

        bom_id = self._bom_search(product=bom_line.product_id,
                                  template=bom_line.product_template)
        items = []
        if bom_id:
            for line in bom_id.bom_line_ids:
                items += self._compute_bom_line(line, product, attributes)

        quantity = bom_line.compute_rule(attributes)
        if isinstance(quantity, bool) or quantity:
            vals = (0, 0, {'product_qty': quantity or bom_line.product_qty,
                           'product_id': bom_line.product_id.id or product.id,
                           'type': 'normal',
                           'product_template': bom_line.product_template.id,
                           'bom_id': bom_line.bom_id.id,
                           'bom_name': bom_line.bom_id.name})
            return items + [vals]
        return items

    @api.multi
    def action_compute_bom_trhough_attributes(self, product=None,
                                              properties=None):
        attributes = [{'id': x.attribute.id, 'name': x.attribute.name,
                       'value': x.value_str} for x in properties]

        products = {self.product_tmpl_id.id: product.id}
        items = []
        for line in self.bom_line_ids:
            prod = product
            if line.product_template.configurator_template:

                attr_values = properties.filtered(
                    lambda x: x.product_tmpl_id.id == line.product_template.id)\
                    .mapped('value')

                prod = self.env['product.product'].create(
                    {'product_tmpl_id': line.product_template.id,
                     'attribute_value_ids': [(6, 0, attr_values.ids)]})
                products[line.product_template.id] = prod.id

            items += self._compute_bom_line(line, prod, attributes)

        keyfunc = lambda x: x[2]['bom_id']

        items = sorted(items, key=keyfunc)
        from itertools import groupby

        agrupados = groupby(items, keyfunc)
        for k, g in agrupados:
            bom = self.env['mrp.bom'].browse(k)
            print bom.name

            new_bom = self.create({
                'name': bom.product_tmpl_id.name,
                'product_tmpl_id': bom.product_tmpl_id.id,
                'product_id': products[bom.product_tmpl_id.id],
                'product_qty': bom.product_qty,
                'type': 'normal'
            })
            new_lines = [x for x in g]
            for x in new_lines:
                x[2]['bom_id'] = new_bom.id
            new_bom.write({'bom_line_ids': new_lines})


class MrpBomExpression(models.Model):
    _name = 'mrp.bom.expression'
    _description = u'Expressão BOM'

    name = fields.Char('Nome', size=20)

    rule_expression = fields.Text('Regra (python)',
                                  default="""# Código python
# Você pode usar as sequintes variáveis:
#  - obj_env: Variavel ORM do objeto atual
#  - bom: lista de materiais que está sendo avaliada
#  - bom_line: linha da lista de materiais que esta sendo avaliada
#  - product: Produto que esta propriedade pertence
#  - attributes: Atributos escolhidos no configurador
#  - env: ORM environment
# ----------------------------------------------------------------
# Retorno:
#  - quantidade: quantidade do material a usar (0 - para remover)
""")


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    bom_name = fields.Char('Nome')
    product_id = fields.Many2one(required=False)
    product_template = fields.Many2one('product.template',
                                       string='Modelo de produto')
    quantity_use = fields.Float(string="Quantidade Calculada", digits=(18, 6))
    expression_ids = fields.Many2many('mrp.bom.expression',
                                      string="Expressões")

    @api.model
    def compute_rule(self, attributes):
        result = self._rule_eval('mrp.bom.line', self.bom_id,
                                 self, attributes)
        return result

    @api.model
    def _exception_rule_eval_context(self, name, bom, bom_line, product,
                                     attributes):
        return {
            'obj_env': self.env[name],
            'bom': bom,
            'bom_line': bom_line,
            'product': product,
            'attributes': attributes,
            'env': self.env,
        }

    @api.model
    def _rule_eval(self, name, bom, bom_line, attributes):
        expressions = bom_line.expression_ids
        space = self._exception_rule_eval_context(
            name, bom, bom_line, bom_line.product_template, attributes)
        try:
            for expr in expressions:
                safe_eval(expr.rule_expression,# nocopy allows to return value
                          space, mode='exec', nocopy=True)
        except Exception as e:
            raise UserError(
                _('Error'),
                _('Error when evaluating the invoice '
                  'rule:\n %s \n(%s)') % (bom.name, e))
        return space.get('quantidade', False)
