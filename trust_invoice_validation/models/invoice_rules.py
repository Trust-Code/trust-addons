# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
#              Danimar Ribeiro <danimaribeiro@gmail.com>                      #
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
#                                                                             #
###############################################################################


from openerp import api, fields, models
from openerp.tools.safe_eval import safe_eval
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class AccountInvoiceRules(models.Model):
    _name = 'account.invoice.rules'

    active = fields.Boolean('Active', default=True)
    name = fields.Char('Name', size=50)
    description = fields.Text('Description')
    sequence = fields.Integer(
        string='Sequence', default=10,
        help="Gives the sequence order when applying the test")

    rule_expression = fields.Text('Regra (python)',
                                  default="""
# Python code. Use failed = True to block the invoice confirmation.
# You can use the following variables :
#  - obj_env: ORM environment of the objet which is used
#  - invoice: invoice is always available
#  - line: line is available if this rule is for the line
#  - env: ORM model environment """)
    message = fields.Char('Validation Message', size=150)

    use_in = fields.Selection([
        ('account.invoice', 'Account Invoice'),
        ('account.invoice.line', 'Account Invoice Line')
    ], string='Use in')

    @api.multi
    def validate(self, invoice, line=False):
        for rule in self:
            if self._rule_eval(rule, rule.use_in, invoice, line):
                raise UserError('Erro de validação!', rule.message)

    @api.model
    def _exception_rule_eval_context(self, obj_name, invoice, line):
        return {
            'obj_env': self.env[obj_name],
            'invoice': invoice,
            'line': line,
            'env': self.env,
        }

    @api.model
    def _rule_eval(self, rule, obj_name, invoice, line):
        expr = rule.rule_expression
        space = self._exception_rule_eval_context(obj_name, invoice, line)
        try:
            safe_eval(expr,
                      space,
                      mode='exec',
                      nocopy=True)  # nocopy allows to return 'result'
        except Exception as e:
            raise UserError(
                _('Error'),
                _('Error when evaluating the invoice '
                  'rule:\n %s \n(%s)') % (rule.name, e))
        return space.get('failed', False)
