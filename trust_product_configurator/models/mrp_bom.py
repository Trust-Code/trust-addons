# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.tools.safe_eval import safe_eval
from openerp.exceptions import Warning as UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

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
                           'product_template': bom_line.product_template.id})
            return items + [vals]
        return items

    @api.multi
    def action_compute_bom_trhough_attributes(self, product=None,
                                              properties=None):
        attributes = [{'id': x.attribute.id, 'name': x.attribute.name,
                       'value': x.value_str} for x in properties]

        items = []
        for line in self.bom_line_ids:
            if line.product_template.configurator_template:

                attr_values = properties.filtered(
                    lambda x: x.product_tmpl_id.id == line.product_template.id)\
                    .mapped('value')

                product = self.env['product.product'].create(
                    {'product_tmpl_id': line.product_template.id,
                     'attribute_value_ids': [(6, 0, attr_values.ids)]})

            items += self._compute_bom_line(line, product, attributes)

        self.create({'name': self.product_tmpl_id.name,
                     'product_tmpl_id': self.product_tmpl_id.id,
                     'product_id': product.id, 'product_qty': 1.0,
                     'type': 'normal', 'bom_line_ids': items})


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_id = fields.Many2one(required=False)
    product_template = fields.Many2one('product.template',
                                       string='Modelo de produto')

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

    quantity_use = fields.Float(string="Quantidade Calculada", digits=(18, 6))

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
        expr = bom_line.rule_expression
        space = self._exception_rule_eval_context(
            name, bom, bom_line, bom_line.product_template, attributes)
        try:
            safe_eval(expr,
                      space,
                      mode='exec',
                      nocopy=True)  # nocopy allows to return 'result'
        except Exception as e:
            raise UserError(
                _('Error'),
                _('Error when evaluating the invoice '
                  'rule:\n %s \n(%s)') % (bom.name, e))
        return space.get('quantidade', False)
