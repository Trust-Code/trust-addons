# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    resin = fields.Selection([
        ('isophthalic', 'Isophthalic'),
        ('off-shore', 'Off-Shore'),
        ('orthophthalic', 'Orthophthalic'),
        ('phynolic', 'Phynolic'),
        ('vinyl ester', 'Vinyl Ester')],
        'Resin', readonly=False, select=True,
        required=True, default="isophthalic")
    fixation = fields.Selection([
        ('stainless steel 304', 'Stainless Steel 304'),
        ('stainless steel 316',
         'Stainless Steel 316'),
        ('stainless steel 316L',
         'Stainless Steel 316L'),
        ], 'Fixation', readonly=False, select=True,
        required=True, default="stainless steel 304")
    color = fields.Selection([
        ('yellow safety', 'Yellow Safety'),
        ('gray', 'Gray'),
        ('yellow safety/gray',
         'Yellow Safety/Gray'),
        ('green', 'Green'),
        ('write', 'Write'),
        ('special', 'Special'),
        ], 'Color', readonly=False, select=True, required=True,
        default="yellow safety/gray")
    special_color = fields.Char('Special Color', size=20,
                                help='Insert here the special color.')
