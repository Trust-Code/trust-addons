# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from datetime import datetime, date
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        vals = {}
        if self.partner_id:
            self.email_from = self.partner_id.email
            self.phone = self.partner_id.phone
            self.mobile = self.partner_id.mobile
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
        string='Contratos Ativos')
    control_time = fields.One2many(comodel_name="account.analytic.line",
                                   inverse_name='control_time_crm',
                                   string="")
    product_id = fields.Many2one(comodel_name="account.analytic.product.line",
                                 inverse_name="product_line_ids",
                                 string="Produto")
    remaining_hours = fields.Float(u'Horas Restantes',
                                   related="product_id.remaining_hours")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and self.product_id.expire:
            expire = datetime.strptime(self.product_id.expire,
                                       DEFAULT_SERVER_DATE_FORMAT)
            if expire.date() < datetime.now().date():
                self.product_id = None
                return {'warning': {
                    'title': 'Atenção!',
                    'message': 'O produto contratado já venceu!'}}
            if self.product_id.remaining_hours <= 0.0:
                return {'warning': {
                    'title': 'Atenção!',
                    'message': 'As horas contratadas acabaram!'}}

    def other_count_time_open(self, user_id):
        state = False
        other_time_open = self.env['account.analytic.line'].search(
            [('user_id', '=', user_id),
             ('time_open', '=', True)],
            order='id desc', limit=1)

        if other_time_open.time_open and \
           other_time_open.control_time_crm.id != self.id:
            state = True
        return state

    def count_time_start(self, vals, stage_name, user_id):
        product_account = self.product_id.product_id.property_account_income
        categ_account = self.product_id.product_id.categ_id.\
            property_account_income_categ
        if not self.account_analytic_id.journal_id:
            raise UserError(u'Configure o diário no contrato')
        if not product_account and not categ_account:
            raise UserError(
                u'Este Produto e a Categoria Não Possuem uma Conta de \
                Receita Cadastrada')
        else:
            account_id = categ_account.id
            if product_account:
                account_id = product_account.id

            self.env['account.analytic.line'].sudo().create(
                {'name': u'Tempo Automático (%s)' % (stage_name),
                 'account_id': self.account_analytic_id.id,
                 'journal_id': self.account_analytic_id.journal_id.id,
                 'date': date.today(),
                 'general_account_id': account_id,
                 'user_id': user_id,
                 'start_date':  datetime.now(),
                 'control_time_crm': self.id,
                 'time_open': True,
                 'ref': self.sequence,
                 'product_id': self.product_id.product_id.id,
                 'discount': self.product_id.discount})

        return

    def count_time_stop(self, stage_name, user_id):
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
            crm_support.amount = crm_support.unit_amount * \
                crm_support.product_id.standard_price
        return

    @api.multi
    def write(self, vals):
        if "stage_id" in vals:
            next_stage = self.env['crm.helpdesk.type'].browse(vals["stage_id"])
            if next_stage.count_time:
                if self.other_count_time_open(self.user_id.id):
                    raise UserError(u"Movimentação não Permitida!",
                                    u"Já existe outra contagem de \
                                    tempo ativa.")
                else:
                    self.count_time_start(vals, next_stage.name,
                                          self.user_id.id)
            else:
                self.count_time_stop(next_stage.name, self.user_id.id)

        elif "user_id" in vals and self.stage_id.count_time:
            self.count_time_start(vals, next_stage.name, self.user_id.id)
        if vals.get('stage_id'):
            stage = self.env['crm.helpdesk.type'].browse(vals['stage_id'])
            if stage.finished:
                vals['state'] = 'done'
            else:
                vals['state'] = 'open'
                vals['date_closed'] = None
        return super(CrmHelpdesk, self).write(vals)
