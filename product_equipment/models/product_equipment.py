# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    CPU = fields.Char('CPU', max_length=100)
    ram_memory = fields.Char('Memória RAM', max_length=100)
    hd_memory = fields.Char('HD', max_length=100)