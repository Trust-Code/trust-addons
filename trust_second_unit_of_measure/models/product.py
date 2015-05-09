'''
Created on May 7, 2015

@author: danimar
'''

from openerp import models, api, fields

class product_template(models.Model):
    _inherit = 'product.template'
    
    second_uom_id = fields.Many2one('product.uom', string="Second Unit of Measure",
                            required=False, help="Second Unit of Measure to control the product Stock. Generally used for industry production.")
    
    use_dimension = fields.Boolean(string="Use Dimension", help="Check if this product requires dimension "
                                "when using BOM or in purchase.")
    
# class product_product(osv.osv):
#     _inherit = "product.product"
#     
#     def _product_available(self, cr, uid, ids, name, arg, context=None):
#         pass
#     
#     def _search_product_quantity(self, cr, uid, obj, name, domain, context):
#         pass
#        
#     qty_available = fields.Float(compute=_product_available, multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Quantity On Hand',
#             search=_search_product_quantity,
#             help="Current quantity of products in the second unit of measure.\n")
#     
#     virtual_available = fields.Float(compute=_product_available, multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Forecast Quantity',
#             search=_search_product_quantity,
#             help="Forecast quantity (computed as Quantity On Hand "
#                  "- Outgoing + Incoming)\n")
#     
#     incoming_qty = fields.Float(compute=_product_available, multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Incoming',
#             search=_search_product_quantity,
#             help="Quantity of products that are planned to arrive.\n")
#     outgoing_qty = fields.Float(compute=_product_available, multi='qty_available',
#             type='float', digits=dp.get_precision('Product Unit of Measure'),
#             string='Outgoing',
#             search=_search_product_quantity,
#             help="Quantity of products that are planned to leave.\n")
#     
    