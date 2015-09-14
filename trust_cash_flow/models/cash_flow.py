# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
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


from openerp import tools
from openerp.osv import fields, osv


class CashFlow(osv.osv):
    _name = "cash.flow.report"
    _description = "Cash Flow Report"
    _auto = False
    _order = 'date_maturity'

    _columns = {
        'date_created': fields.date('Create Date', readonly=True),
        'date': fields.date('Move Date', readonly=True),
        'date_maturity': fields.date('Due Date', readonly=True),

        'statement_id': fields.many2one('account_bank_statement',
                                        'Bank Statement', readonly=True),
        'journal_id': fields.many2one('account.jornal', 'Journal',
                                      readonly=True),

        'debit': fields.float(u'Débito', readonly=True),
        'credit': fields.float(u'Crédito', readonly=True),
        
        'total': fields.float(u'Acumulado dia', readonly=True),

        'reference': fields.char('Reference', readonly=True),
        'name': fields.char('Name', readonly=True),

        'move_id': fields.many2one('account.move', 'Account Move',
                                   readonly=True),

        'product_id': fields.many2one('product.product', 'Product',
                                      readonly=True),
        'product_uom_id': fields.many2one('product.uom', 'Unit of Measure',
                                          readonly=True),

        'partner_id': fields.many2one('res.partner', 'Partner', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'user_id': fields.many2one('res.users', 'Salesperson', readonly=True),

        'nbr_lines': fields.integer('# of Lines', readonly=True),

        'state': fields.selection([('draft', 'Unbalanced'),
                                   ('valid', 'Balanced')],
                                  'Order Status', readonly=True),

        'analytic_account_id': fields.many2one(
            'account.analytic.account',
            'Analytic Account', readonly=True),
    }
    _order = 'date desc'

    def _select(self):
        select_str = """
            SELECT aml.id, statement_id, aml.company_id, date_maturity,
                   partner_id, analytic_account_id,
                   credit, journal_id,
                   tax_code_id, state, debit, ref as reference, account_id, period_id,
                   date_created, date, move_id, aml.name, reconcile_id, tax_amount,
                   product_id, account_tax_id, product_uom_id, amount_currency,
                   quantity
        """
        return select_str

    def _from(self):
        from_str = """
                account_move_line aml
                    inner join account_account ac on aml.account_id = ac.id
        """
        return from_str

    def _where(self):
        where_str = """
            where ac.type = 'receivable' or ac.type = 'payable'
        """
        return where_str

    def _group_by(self):
        group_by_str = """
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            SELECT subq.*, sum(debit) OVER (ORDER BY date_maturity) as total
            FROM (
            %s FROM ( %s ) %s  %s order by date_maturity desc) as subq)""" % (
            self._table, self._select(), self._from(), self._where(),
            self._group_by()))
