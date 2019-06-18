# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import datetime
import openerp.addons.decimal_precision as dp
from openerp import api, fields, models


class CashFlowReport(models.TransientModel):
    _name = 'account.cash.flow'
    _description = u'Cash Flow Report'

    @api.one
    def calc_final_amount(self):
        balance = 0
        for line in self.line_ids:
            balance += line.amount
        balance += self.start_amount
        self.final_amount = balance

    company_id = fields.Many2one('res.company', string="Empresa")
    start_date = fields.Date(string="Start Date", required=True,
                             default=fields.date.today())
    end_date = fields.Date(
        string="End Date", required=True,
        default=fields.date.today()+datetime.timedelta(6*365/12))
    start_amount = fields.Float(string="Initial Value",
                                digits_compute=dp.get_precision('Account'))
    final_amount = fields.Float(string="Total",
                                compute="calc_final_amount",
                                digits_compute=dp.get_precision('Account'))
    line_ids = fields.One2many(
        "account.cash.flow.line", "cashflow_id",
        string="Cash Flow Lines")

    @api.multi
    def calculate_liquidity(self):
        accs = self.env['account.account'].with_context(state='posted').search(
            [('type', '=', 'liquidity'),
             ('company_id', '=', self.company_id.id)])
        liquidity_lines = []
        for acc in accs:
            if acc.balance != 0:
                liquidity_lines.append({
                    'name': acc.name or '-',
                    'cashflow_id': self.id,
                    'account_id': acc.id,
                    'debit': acc.credit,
                    'credit': acc.debit,
                    'amount': acc.balance,
                })
        return liquidity_lines

    @api.multi
    def calculate_moves(self):
        moveline_obj = self.env['account.move.line']
        moveline_ids = moveline_obj.search([
            '|',
            ('account_id.type', '=', 'receivable'),
            ('account_id.type', '=', 'payable'),
            ('reconcile_id', '=', False),
            ('state', '!=', 'draft'),
            ('company_id', '=', self.company_id.id),
            ('date_maturity', '<=', self.end_date),
        ])
        moves = []
        for move in moveline_ids:
            debit, credit = move.credit, move.debit
            amount = move.debit - move.credit
            if move.reconcile_partial_id:
                move_ids = moveline_obj.search(
                    [('reconcile_partial_id', '=',
                      move.reconcile_partial_id.id)])
                debit = sum(line.credit for line in move_ids)
                credit = sum(line.debit for line in move_ids)
                amount = credit - debit

            moves.append({
                'name': move.ref or '-',
                'cashflow_id': self.id,
                'partner_id': move.partner_id.id,
                'journal_id': move.journal_id.id,
                'account_id': move.account_id.id,
                'date': move.date_maturity,
                'debit': debit,
                'credit': credit,
                'amount': amount,
            })
        return moves

    @api.multi
    def action_calculate_report(self):
        self.write({'line_ids': [(5, 0, 0)]})
        balance = self.start_amount
        liquidity_lines = self.calculate_liquidity()
        move_lines = self.calculate_moves()

        move_lines.sort(key=lambda x: datetime.datetime.strptime(x['date'],
                                                                 '%Y-%m-%d'))

        for lines in liquidity_lines+move_lines:
            balance += lines['credit'] - lines['debit']
            lines['balance'] = balance
            self.env['account.cash.flow.line'].create(lines)


class CashFlowReportLine(models.TransientModel):
    _name = 'account.cash.flow.line'
    _description = u'Cash flow lines'

    name = fields.Char(string="Description", required=True)
    date = fields.Date(string="Date")
    partner_id = fields.Many2one("res.partner", string="Partner")
    account_id = fields.Many2one("account.account", string="Account")
    journal_id = fields.Many2one("account.journal", string="Journal")
    invoice_id = fields.Many2one("account.invoice", string="Invoice")
    debit = fields.Float(string="Debit",
                         digits_compute=dp.get_precision('Account'))
    credit = fields.Float(string="Credit",
                          digits_compute=dp.get_precision('Account'))
    amount = fields.Float(string="Balance(C-D)",
                          digits_compute=dp.get_precision('Account'))
    balance = fields.Float(string="Accumulated Balance",
                           digits_compute=dp.get_precision('Account'))
    cashflow_id = fields.Many2one("account.cash.flow", string="Cash Flow")
