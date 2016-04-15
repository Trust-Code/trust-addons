# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.tools.safe_eval import safe_eval
from openerp.exceptions import Warning as UserError


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
#  - env: ORM environment
# ----------------------------------------------------------------
# Retorno:
#  - quantidade: quantidade do material a usar (0 - para remover)
""")

    quantity_use = fields.Float(string="Quantidade Calculada", digits=(18, 6))

    @api.multi
    def compute_rule(self, attributes):
        for bom_line in self:
            result = self._rule_eval('mrp.bom.line', bom_line.bom_id,
                                     bom_line, attributes)
            bom_line.quantity_use = result

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
        expr = bom.rule_expression
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
        return space.get('failed', False)
