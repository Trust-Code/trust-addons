# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 Trustcode - www.trustcode.com.br                         #
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

from datetime import date
from openerp import api, fields, models
from openerp.addons import decimal_precision as dp
from dateutil.relativedelta import relativedelta


class CompanyMonthlyRevenue(models.Model):
    _name = 'res.company.monthly.revenue'
    _order = 'year desc, month desc'

    company_id = fields.Many2one('res.company', string="Empresa")
    month = fields.Integer(string="Mês", required=True)
    year = fields.Integer(string="Ano", required=True)
    revenue = fields.Float(string="Faturamento Mês",
                           precision=(18, 6), required=True)


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.depends('monthly_revenue_ids')
    def _calculate_total_revenue(self):
        for rec in self:
            count = 0
            total = 0.0
            for month in rec.monthly_revenue_ids.sorted():
                count += 1
                total += month.revenue
                if count >= 12:
                    break
            rec.annual_revenue = total

    annual_revenue = fields.Float(
        'Faturamento Anual', required=True,
        digits_compute=dp.get_precision('Account'), default=0.00,
        help="Faturamento Bruto dos últimos 12 meses",
        compute=_calculate_total_revenue, store=True)

    monthly_revenue_ids = fields.One2many('res.company.monthly.revenue',
                                          'company_id',
                                          string=u"Receitas mensais")

    @api.model
    def calculate_revenue_monthly(self):

        def get_month_day_range(date):
            last_day = date + relativedelta(day=1, months=+1, days=-1)
            first_day = date + relativedelta(day=1)
            return first_day, last_day

        for company in self.search([('fiscal_type', '!=', '3')]):
            sql = """select sum(amount_total) from account_invoice
                where date_invoice between %s and %s and company_id = %s
                and state in ('open', 'paid')"""

            today = date.today()
            first, last = get_month_day_range(today)
            self.env.cr.execute(sql, (first, last, company.id))
            total_revenue = self.env.cr.fetchone()[0] or 0.0

            env_month = self.env['res.company.monthly.revenue']
            current_month = env_month.search([('month', '=', today.month),
                                              ('year', '=', today.year),
                                              ('company_id', '=', company.id)])
            if current_month:
                current_month.revenue = total_revenue
            else:
                env_month.create({'month': today.month, 'year': today.year,
                                  'revenue': total_revenue,
                                  'company_id': company.id})
