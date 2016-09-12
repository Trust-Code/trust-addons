

from openerp import api, models


class StockTransferDetails(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.model
    def default_get(self, fields):
        res = super(StockTransferDetails, self).default_get(fields)

        picking_ids = self.env.context.get('active_ids', [])
        picking_id, = picking_ids
        picking = self.env['stock.picking'].browse(picking_id)
        for op in picking.move_lines:
            if op.state == 'cancel':
                item = filter(
                    lambda x: x['sourceloc_id'] == op.location_id.id and
                    x['destinationloc_id'] == op.location_dest_id.id and
                    x['product_id'] == op.product_id.id and
                    x['quantity'] == op.product_uom_qty, res['item_ids'])
                res['item_ids'].remove(item[0])
        return res
