'''
Created on 3 de fev de 2016

@author: danimar
'''


from openerp import api, fields, models


class SaleOrderConfiguredProducts(models.Model):
    _name = 'sale.order.configured.product'
    _description = 'Configured Products in Sales Order'

    sale_order_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    order_line_id = fields.Many2one('sale.order.line', 
                                    string="Sale Order Line Related",
                                    readonly=True)

    product_tmpl_id = fields.Many2one(
        'product.template',
        domain="[('configurator_template', '=', True)]")
    
    quantity = fields.Integer(string="Quantity")    
    
