# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import datetime
import openerp.addons.decimal_precision as dp
from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DSDT
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DSDTT


class CashFlowReport(models.TransientModel):
    _inherit = 'cash.flow'

    include_confirmed_quotations = fields.Boolean("Incluir Cotações?")

    def _search_purchase(self):
        purchase_obj = self.env['purchase.order']
        purchase_ids = purchase_obj.search([
            ('state', '=', 'approved'),
            ('company_id', '=', self.env.user.company_id.id),
            ('minimum_planned_date', '>=', self.start_date),
            ('minimum_planned_date', '<=', self.end_date),
        ])
        moves = []
        for purchase in purchase_ids:
            moves.append({
                'name': purchase.name,
                'cashflow_id': self.id,
                'partner_id': purchase.partner_id.id,
                'account_id': purchase.partner_id.property_account_payable.id,
                'date': purchase.minimum_planned_date,
                'debit': 0.0 - purchase.amount_total,
                'credit': 0.0,
                'amount': 0.0 - purchase.amount_total,
            })
        return moves

    def _search_sales(self):
        start_datetime = datetime.datetime.strptime(self.start_date, DSDT)
        end_datetime = datetime.datetime.strptime(self.end_date, DSDT)

        sale_obj = self.env['sale.order']
        sale_ids = sale_obj.search([
            ('state', '=', 'manual'),
            ('company_id', '=', self.env.user.company_id.id),
            ('commitment_date', '>=', start_datetime.strftime(DSDT)),
            ('commitment_date', '<=', end_datetime.strftime(DSDT)),
        ])
        moves = []
        for sale in sale_ids:
            date = datetime.datetime.strptime(sale.commitment_date, DSDTT)
            moves.append({
                'name': sale.name,
                'cashflow_id': self.id,
                'partner_id': sale.partner_id.id,
                'account_id': sale.partner_id.property_account_receivable.id,
                'date': date.strftime(DSDT),
                'debit': 0.0,
                'credit': sale.amount_total,
                'amount': sale.amount_total,
            })
        return moves

    @api.multi
    def calculate_moves(self):
        result = super(CashFlowReport, self).calculate_moves()

        if self.include_confirmed_quotations:
            result += self._search_sales()
            result += self._search_purchase()
        return result
