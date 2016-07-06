# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class HrAnalyticTimesheet(models.Model):
    _inherit = 'hr.analytic.timesheet'

    pay_overtime = fields.Boolean(string='Hora Extra')
