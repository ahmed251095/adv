from odoo import api, fields, models


class moveOrderLineInheritTime(models.Model):
    _inherit = "account.move.line"
    amount_discount = fields.Monetary(string='Discount',
                                      readonly=True, compute='_compute_price_subtotal')

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'duration')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_unit = line.product_id.list_price
            line.price_subtotal = float(line.price_unit) * float(line.quantity)
            if line.duration or line.product_price:
                line.price_unit = line.product_price * line.duration
                line.price_subtotal = float(line.price_unit) * float(line.quantity) * (100 - line.discount) / 100
                line.amount_discount = ( line.quantity * line.price_unit) * (100 - line.discount) / 100
