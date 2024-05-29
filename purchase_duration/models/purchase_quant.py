from odoo import api, fields, models

class SaleOrderLineInheritTime(models.Model):

    _inherit = "sale.order.line"

    duration = fields.Float(string="المدة",default=1)
    product_price = fields.Float(related='product_id.list_price')
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','duration')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        This is the method where price computation is typically done.
        """
        super(SaleOrderLineInheritTime, self)._compute_amount()
        for line in self:
            line.price_unit = line.product_id.list_price
            line.price_subtotal = float(line.price_unit) * float(line.product_uom_qty)
            if line.duration:
                line.price_unit = line.price_unit * line.duration
                line.price_subtotal = float(line.price_unit) * float(line.product_uom_qty)
