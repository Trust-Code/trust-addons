# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime


class AccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    contract_guarantee = fields.Boolean(string='Contrato Suporte / Garantia')
    generic_contract = fields.Boolean(
        string='Contrato Genérico para Clientes sem Contratos')
    product_line_ids = fields.One2many(
        comodel_name="account.analytic.product.line",
        inverse_name='account_analytic_id', string="Produtos")
    crm_helpdesk_id = fields.One2many(comodel_name='crm.helpdesk',
                                      inverse_name='account_analytic_id')
    journal_id = fields.Many2one(comodel_name='account.analytic.journal',
                                 relation='analytic_account_id',
                                 string='Diário Padrão')


class AccountAnalyticJournal(models.Model):
    _inherit = "account.analytic.journal"

    analytic_account_ids = fields.One2many(
        comodel_name='account.analytic.account',
        inverse_name='journal_id', string="Contas Analíticas")


class AccountAnalyticProductLine(models.Model):
    _name = "account.analytic.product.line"

    @api.multi
    def name_get(self):
        return [(rec.id, rec.product_id.name) for rec in self]

    @api.onchange("product_id")
    def _onchange_product_id(self):
        un_id = self.product_id.uom_id
        un = self.env['product.uom'].browse(un_id)
        self.product_uom_id = un.id

    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Serviço / Produto Incluso')
    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Contrato')
    product_uom_id = fields.Many2one(comodel_name="product.uom",
                                     string="Unidade")
    quantity = fields.Float(string="Quantidade")
    discount = fields.Float(string="Desconto %")
    expire = fields.Date(string="Data de Vencimento")
    crm_support_product_id = fields.One2many(comodel_name='crm.helpdesk',
                                             inverse_name='product_id')


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.depends("start_date", "end_date")
    def _compute_amount_time(self):
        for item in self:
            if item.start_date and item.end_date:
                start = datetime.strptime(item.start_date,
                                          DEFAULT_SERVER_DATETIME_FORMAT)
                end = datetime.strptime(item.end_date,
                                        DEFAULT_SERVER_DATETIME_FORMAT)
                total = (end - start)
                total_hours = float(total.seconds)/3600
                item.unit_amount = total_hours

    start_date = fields.Datetime(string="Data Inicio")
    discount = fields.Float(string="Desconto %")
    end_date = fields.Datetime(string="Data Final")
    control_time_crm = fields.Many2one(comodel_name='crm.helpdesk',
                                       inverse_name='control_time')
    time_open = fields.Boolean("Contando tempo")
    unit_amount = fields.Float(
        'Quantity', default=0.0, compute=_compute_amount_time, store=True)
