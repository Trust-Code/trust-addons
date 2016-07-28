# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    tasks_categ = fields.Many2many(comodel_name='project.category',
                                   string="Funções")
