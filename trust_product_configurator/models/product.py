# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from openerp import api, fields, models, _
from openerp.tools.safe_eval import safe_eval
from openerp.exceptions import Warning as UserError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attr_type = fields.Selection(required=True, selection=[
        ('selection', 'Select'),
        ('integer', 'Integer'),
        ('float', 'Numeric'),
        ('char', 'Text'),
        ('boolean', 'Boolean')], string="Type", default='selection')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    configurator_template = fields.Boolean('Template do configurador?',
                                           default=False)


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    name = fields.Char('Value')
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
