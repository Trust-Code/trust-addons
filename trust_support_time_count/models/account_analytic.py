# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, date
from openerp.exceptions import Warning


class AccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    contract_guarantee = fields.Boolean(string='Contrato Suporte / Garantia')
    generic_contract = fields.Boolean(
        string='Contrato Genérico para Clientes sem Contratos')
    product_line = fields.One2many(
        comodel_name="account.analytic.product.line",
        inverse_name='account_analytic_id', string="")
    crm_helpdesk_id = fields.One2many(comodel_name='crm.helpdesk',
                                      inverse_name='account_analytic_id')
    journal_id = fields.Many2one(comodel_name='account.analytic.journal',
                                 relation='analytic_account_id',
                                 string='Diário Padrão')


class AccountAnalyticJournal(models.Model):
    _inherit = "account.analytic.journal"

    analytic_account_id = fields.One2many(
        comodel_name='account.analytic.account',
        inverse_name='journal_id')


class AccountAnalyticProductLine(models.Model):
    _name = "account.analytic.product.line"

    @api.multi
    def name_get(self):
        return [(rec.id, rec.product_id.name) for rec in self]

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.product_uom_id = self.product_id.uom_id.id

    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Serviços / Produtos Inclusos')
    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Serviços / Produtos Inclusos')
    product_uom_id = fields.Many2one(comodel_name="product.template",
                                     string="Unidade")
    quantity = fields.Float(string="Quantidade")
    discount = fields.Float(string="Desconto %")
    expire = fields.Date(string="Data de Vencimento")
    crm_support_product_id = fields.One2many(comodel_name='crm.helpdesk',
                                             inverse_name='product_id')


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    @api.onchange("partner_id")
    def _onchange_field(self):
        vals = {}
        if self.partner_id:
            account_analytic_id_search = self.env['account.analytic.account'].\
                search([('partner_id', '=', self.partner_id.id)], limit=1)

            if not account_analytic_id_search:
                generic_contract = self.env['account.analytic.account'].search(
                    [('generic_contract', '=', True)])
                if generic_contract:
                    self.account_analytic_id = generic_contract[0]

            if account_analytic_id_search:
                self.account_analytic_id = account_analytic_id_search[0]

            if not account_analytic_id_search and not generic_contract:
                vals['warning'] = {
                    'title': ('Erro de Contrato'),
                    'message': ('Este cliente não possui um contrato, e não \
                                existe um Contrato Genérico.')
                }

            return vals
    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        inverse_name="crm_helpdesk_id",
        string='Contratos Ativos', required=True)
    control_time = fields.One2many(comodel_name="account.analytic.line",
                                   inverse_name='control_time_crm',
                                   string="")
    product_id = fields.Many2one(comodel_name="account.analytic.product.line",
                                 inverse_name="product_line",
                                 required="True",
                                 string="Produto")

    def other_count_time_open(self, user_id):
        state = False
        other_time_open = self.env['account.analytic.line'].search(
            [('user_id', '=', user_id),
             ('time_open', '=', True)],
            order='id desc', limit=1)

        if other_time_open.time_open and other_time_open.task_id.id != self.id:
            state = True
        return state

    def count_time_start(self, vals, stage_name, user_id):
        product_account = self.product_id.product_id.property_account_income
        categ_account = self.product_id.product_id.categ_id.\
            property_account_income_categ
        if not product_account and categ_account:
            raise Warning(
                u'Este Produto E A Sua Categoria Não Possuem uma Conta de \
                Receita Cadastrad')
        else:
            if product_account:
                self.env['account.analytic.line'].sudo().create(
                    {'name': u'Tempo Automático (%s)' % (stage_name),
                     'account_id': self.account_analytic_id.id,
                     'journal_id': self.account_analytic_id.journal_id.id,
                     'date': date.today(),
                     'amount':  self.product_id.product_id.lst_price,
                     'general_account_id': product_account.id,
                     'user_id': user_id,
                     'start_date':  datetime.now(),
                     'control_time_crm': self.id,
                     'time_open': True})
            else:
                self.env['account.analytic.line'].sudo().create(
                    {'name': u'Tempo Automático (%s)' % (stage_name),
                     'account_id': self.account_analytic_id.id,
                     'journal_id': self.account_analytic_id.journal_id.id,
                     'date': date.today(),
                     'amount':  self.product_id.product_id.lst_price,
                     'general_account_id': categ_account.id,
                     'user_id': user_id,
                     'start_date':  datetime.now(),
                     'control_time_crm': self.id,
                     'time_open': True})

        return

    def count_time_stop(self, stage_name, user_id):
        # import ipdb; ipdb.set_trace()
        crm_support = self.env['account.analytic.line'].sudo().search(
            [('user_id', '=', user_id),
             ('time_open', '=', True),
             ('control_time_crm', '=', self.id)], limit=1)
        crm_support.write(
            {
                'end_date':  datetime.now(),
            }
        )
        if crm_support:
            ff = DEFAULT_SERVER_DATE_FORMAT
            count_time = datetime.now() - datetime.strptime(crm_support.date,
                                                            ff)

            crm_support.hours = count_time.total_seconds() / 60.0 / 60.0
            crm_support.time_open = False
        return

    @api.multi
    def write(self, vals):
        if "stage_id" in vals:
            next_stage = self.env['crm.helpdesk.type'].browse(vals["stage_id"])
            if next_stage.count_time:
                if self.other_count_time_open(self.user_id.id):
                    raise Warning(u"Movimentação não Permitida!",
                                  u"Já existe outra contagem de tempo ativa.")
                else:
                    self.count_time_start(vals, next_stage.name,
                                          self.user_id.id)
            else:
                self.count_time_stop(next_stage.name, self.user_id.id)

        elif "user_id" in vals and self.stage_id.count_time:
            self.count_time_start(vals, next_stage.name, self.user_id.id)

        return super(CrmHelpdesk, self).write(vals)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.onchange("end_date")
    def _onchange_end_date(self):
        if self.start_date and self.end_date:
            start = datetime.strptime(self.start_date,
                                      DEFAULT_SERVER_DATETIME_FORMAT)
            end = datetime.strptime(self.end_date,
                                    DEFAULT_SERVER_DATETIME_FORMAT)
            total = (end - start)
            total_hours = float(float(total.seconds)/3600)
            self.unit_amount = total_hours

    start_date = fields.Datetime(string="Data Inicio")
    discount = fields.Float(string="Desconto %")
    end_date = fields.Datetime(string="Data Final")
    control_time_crm = fields.Many2one(comodel_name='crm.helpdesk',
                                       inverse_name='control_time')
    time_open = fields.Boolean()
