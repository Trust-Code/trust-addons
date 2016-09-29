# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    numero_aedf = fields.Char('Número AEDF', size=10)
