# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# Deferral Method    Action
# None               Nothing will be transferred (typically P&L accounts)
# Balance            Account balance will be transferred
#                   (typically Balance Sheet accounts)
# Detail             All entries are transferred, also reconciled entries
# Unreconciled       Only entries that are not reconciled on the first day
#                   of the new financial year will be transferred
#                   (typically receivable and payable)

import datetime
import openerp.addons.decimal_precision as dp
from openerp import api, fields, models


class CashFlowReport(models.Model):
    _name = 'cash.flow'
    _description = u'Relatório de Fluxo de Caixa'

    @api.one
    def calc_final_amount(self):
        balance = 0
        for line in self.line_ids:
            balance += line.amount
        balance += self.start_amount
        self.final_amount = balance

    name = fields.Char(string="Descrição", required=True)
    start_date = fields.Date(string="Data Inicio", required=True,
                             default=fields.date.today())
    end_date = fields.Date(
        string="Data Fim", required=True,
        default=fields.date.today()+datetime.timedelta(6*365/12))
    start_amount = fields.Float(string="Valor Inicial",
                                digits_compute=dp.get_precision('Account'))
    final_amount = fields.Float(string="Valor Final",
                                compute="calc_final_amount",
                                digits_compute=dp.get_precision('Account'))
    line_ids = fields.One2many(
        "cash.flow.line", "cashflow_id",
        string="Linhas Fluxo de Caixa")

    @api.multi
    def calculate_liquidity(self):
        accs = self.env['account.account'].search([('type', '=', 'liquidity')])
        liquidity_lines = []
        for acc in accs:
            if acc.balance != 0:
                liquidity_lines.append({
                    'name': acc.name,
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
            ('company_id', '=', self.env.user.company_id.id),
            ('date_maturity', '<=', self.end_date),
        ])
        moves = []
        for move in moveline_ids:
            moves.append({
                'name': move.ref,
                'cashflow_id': self.id,
                'partner_id': move.partner_id.id,
                'journal_id': move.journal_id.id,
                'account_id': move.account_id.id,
                'date': move.date_maturity,
                'debit': move.credit,
                'credit': move.debit,
                'amount': move.debit - move.credit,
            })
        return moves

    @api.multi
    def button_calculate(self):
        self.write({'line_ids': [(5, 0, 0)]})
        balance = self.start_amount
        liquidity_lines = self.calculate_liquidity()
        move_lines = self.calculate_moves()

        move_lines.sort(key=lambda x: datetime.datetime.strptime(x['date'],
                                                                 '%Y-%m-%d'))

        for lines in liquidity_lines+move_lines:
            balance += lines['credit'] - lines['debit']
            lines['balance'] = balance
            self.env['cash.flow.line'].create(lines)


class CashFlowReportLine(models.Model):
    _name = 'cash.flow.line'

    name = fields.Char(string="Descrição", required=True)
    date = fields.Date(string="Data")
    partner_id = fields.Many2one("res.partner", string="Parceiro")
    account_id = fields.Many2one("account.account", string="Conta")
    journal_id = fields.Many2one("account.journal", string="Diário")
    invoice_id = fields.Many2one("account.invoice", string="Fatura")
    debit = fields.Float(string="Débito",
                         digits_compute=dp.get_precision('Account'))
    credit = fields.Float(string="Crédito",
                          digits_compute=dp.get_precision('Account'))
    amount = fields.Float(string="Saldo(C-D)",
                          digits_compute=dp.get_precision('Account'))
    balance = fields.Float(string="Saldo Acumulado",
                           digits_compute=dp.get_precision('Account'))
    cashflow_id = fields.Many2one("cash.flow",
                                  string="Fluxo de Caixa")
