# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    serasa_login = fields.Char(max_length=30, string="Cliente do Correio")
    serasa_password = fields.Char(max_length=30, string="Senha do Correio")
