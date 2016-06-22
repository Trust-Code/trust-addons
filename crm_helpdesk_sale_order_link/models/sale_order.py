# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    crm_help_id = fields.Many2one('crm.helpdesk')
