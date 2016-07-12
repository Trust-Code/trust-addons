# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        receivable = vals.get("property_account_receivable", False)
        payable = vals.get("property_account_payable", False)
        cliente = 'property_account_receivable'
        fornecedor = 'property_account_payable'

        def copy_account(self, tipo, pg_rc):
            values_account = {
                'name': tipo.name,
                'code': tipo.code,
                'parent_id': tipo.parent_id.id,
                'type': tipo.type,
                'user_type': tipo.user_type.id,
                'reconcile': tipo.reconcile,
                }
            values_account['name'] = vals['name']
            count = self.env['account.account'].search_count(
                [('parent_id', '=', tipo.id)]
            )
            "{0:02d}".format(count)
            values_account['code'] = tipo.code + "." + str(count + 1)
            contaNova = self.env['account.account'].create(values_account)
            vals[pg_rc] = contaNova.id
            return values_account

        if not receivable and self.env.user.company_id.account_bool:
            copy_account(self, self.env.user.company_id.account_receivable, cliente)

        if not payable and self.env.user.company_id.account_bool:
            copy_account(self, self.env.user.company_id.account_payable, fornecedor)

        return super(ResPartner, self).create(vals)


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_bool = fields.Boolean(string="Criar uma conta para cada cliente?")

    account_receivable = fields.Many2one('account.account',
                                         string="Selecione a conta base para\
                                         recebimento")

    account_payable = fields.Many2one('account.account',
                                      string="Selecione a conta base para\
                                      pagamento")


class AccountConfig(models.TransientModel):
    _inherit = 'base.config.settings'

    account_bool = fields.Boolean(string="Criar uma conta para cada cliente?")

    account_receivable = fields.Many2one('account.account',
                                         string="Selecione a conta base para\
                                         recebimento")

    account_payable = fields.Many2one('account.account',
                                      string="Selecione a conta base para\
                                      pagamento")

    def get_default_account_bool(
            self, cr, uid, fields, context=None):
        user = self.pool['res.users'].browse(cr, uid, uid, context)
        return {'account_bool':
                user.company_id.account_bool}

    @api.multi
    def set_account_bool(self):
        self.env.user.company_id.account_bool = self.account_bool

    def get_default_account_receivable(
            self, cr, uid, fields, context=None):
        user = self.pool['res.users'].browse(cr, uid, uid, context)
        return {'account_receivable':
                user.company_id.account_receivable.id}

    @api.multi
    def set_account_receivable(self):
        self.env.user.company_id.account_receivable = self.account_receivable

    def get_default_account_payable(self, cr, uid, fields, context=None):
        user = self.pool['res.users'].browse(cr, uid, uid, context)
        return {'account_payable': user.company_id.account_payable.id}

    @api.multi
    def set_account_payable(self):
        self.env.user.company_id.account_payable = self.account_payable
