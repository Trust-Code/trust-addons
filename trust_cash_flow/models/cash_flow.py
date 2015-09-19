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
    _order = 'date_maturity, id'

    _columns = {
        'date_created': fields.date('Create Date', readonly=True),
        'date': fields.date('Move Date', readonly=True),
        'date_maturity': fields.date('Due Date', readonly=True),

        'statement_id': fields.many2one('account.bank.statement',                                        
                                        'Bank Statement', readonly=True),
        'last_closing_balance': fields.related(
                                        'statement_id',
                                        'last_closing_balance',
                                        type="float",                                        
                                        string="Saldo", readonly=True),
        'journal_id': fields.many2one('account.journal', 'Journal',
                                      readonly=True),
        'account_id': fields.many2one('account.account', 'Account',
                                      readonly=True),

        'debit': fields.float(u'Receber', readonly=True),
        'credit': fields.float(u'Pagar', readonly=True),

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

    def _select(self):
        select_str = """
            SELECT aml.id, statement_id, aml.company_id,
            coalesce(date_maturity, date, date_created) as date_maturity,
            partner_id, analytic_account_id,
            credit, journal_id, tax_code_id, state, debit,
            ref as reference, account_id, period_id,
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
            where ac.type = 'receivable' or ac.type = 'payable' or ac.type = 'liquidity' 
        """
        return where_str

    def _group_by(self):
        group_by_str = """
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        
        cr.execute(""" 
        
        CREATE or REPLACE VIEW %s as (
        SELECT subq.*,  sum(subq.debit - subq.credit) OVER (ORDER BY subq.date_maturity, subq.id) AS total
   FROM (select row_number() OVER ()  as id, null as statement_id, 1 as company_id, current_date as date_maturity, null as partner_id,  
    null as analytic_account_id,  sum(credit)as credit, max(journal_id) as journal_id,  null as tax_code_id,   null as state,   
    sum(debit) as debit,  aj.name AS reference,  aml.account_id,
    null as period_id,  null as date_created, null as date,null as move_id, null as name, null as reconcile_id,null as tax_amount, null as product_id,
    null as account_tax_id,    null as product_uom_id,    null as amount_currency,    null as quantity    
    FROM account_move_line aml
    JOIN account_account ac ON aml.account_id = ac.id
    JOIN account_journal aj ON aml.journal_id = aj.id
  WHERE ac.type = 'liquidity'
  group by journal_id, reference, aml.account_id
union all
  SELECT aml.id,  aml.statement_id,   aml.company_id, COALESCE(aml.date_maturity, aml.date, aml.date_created) AS date_maturity,  aml.partner_id,
    aml.analytic_account_id,  aml.credit,  aml.journal_id,    aml.tax_code_id,    aml.state,    aml.debit,    aml.ref AS reference,    aml.account_id,
    aml.period_id,    aml.date_created,    aml.date,    aml.move_id,    aml.name,    aml.reconcile_id,    aml.tax_amount,    aml.product_id,
    aml.account_tax_id,    aml.product_uom_id,    aml.amount_currency,    aml.quantity
    FROM account_move_line aml
   JOIN account_account ac ON aml.account_id = ac.id
  WHERE (ac.type = 'receivable' OR ac.type = 'payable') and date_maturity >= current_date
  ORDER BY date_maturity DESC) subq
        )
        
        """ % self._table)
        
        #cr.execute("""CREATE or REPLACE VIEW %s as (
        #    SELECT subq.*, sum(debit - credit)
        #    OVER (ORDER BY date_maturity, id) as total
        #    FROM (
        #    %s FROM ( %s ) %s  %s order by date_maturity desc) as subq)""" % (
        #    self._table, self._select(), self._from(), self._where(),
        #    self._group_by()))
