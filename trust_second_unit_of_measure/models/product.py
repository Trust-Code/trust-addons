# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from openerp import models, fields


class product_template(models.Model):
    _inherit = 'product.template'

    second_uom_id = fields.Many2one(
        'product.uom',
        string="Second Unit of Measure",
        required=False, help="Second Unit of Measure"
        "to control the product Stock. Generally used"
        "or industry production."
    )

    use_dimension = fields.Boolean(
        string="Use Dimension",
        help="Check if this product requires "
        "dimension when using BOM or in purchase."
    )

# class product_product(osv.osv):
#     _inherit = "product.product"
#
#     def _product_available(self, cr, uid, ids, name, arg, context=None):
#         pass
#
#     def _search_product_quantity(self, cr, uid, obj, name, domain, context):
#         pass
#
#     qty_available = fields.Float(compute=_product_available,
# multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Quantity On Hand',
#             search=_search_product_quantity,
#             help="Current quantity of products in the second unit
#  of measure.\n")
#
#     virtual_available = fields.Float(compute=_product_available,
#     multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Forecast Quantity',
#             search=_search_product_quantity,
#             help="Forecast quantity (computed as Quantity On Hand "
#                  "- Outgoing + Incoming)\n")
#
#     incoming_qty = fields.Float(compute=_product_available,
#   multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Incoming',
#             search=_search_product_quantity,
#             help="Quantity of products that are planned to arrive.\n")
#     outgoing_qty = fields.Float(compute=_product_available,
#     multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Outgoing',
#             search=_search_product_quantity,
#             help="Quantity of products that are planned to leave.\n")
#
