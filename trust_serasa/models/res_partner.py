# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    status_serasa = fields.Char(max_length=30, string="Status no Serasa",
                                readonly=True)
