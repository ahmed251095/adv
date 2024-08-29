from odoo import api, fields, models
class SaleOrder(models.Model):
    _inherit = "sale.order"

    amount_discount = fields.Monetary(string='اجمالي السعر بعد الخصم', store=True,
                                      readonly=True, compute='_amount_all')

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_discount = 0.0
            for line in order.order_line:
                line.amount_discount = (line.product_uom_qty * line.price_unit) * (100 - line.discount) / 100

            order.update({
                'amount_discount': amount_discount,

            })

class SaleOrderLineInheritTime(models.Model):

    _inherit = "sale.order.line"

    duration = fields.Float(string="المدة",default=1)
    product_price = fields.Float(related='product_id.list_price',readonly=False)
    amount_discount = fields.Monetary(string='Discount', store=True,
                                      readonly=True, compute='_compute_amount')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id','duration','product_price')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        This is the method where price computation is typically done.
        """
        amount_discount = 0.0
        super(SaleOrderLineInheritTime, self)._compute_amount()
        # for line in self:
        #     line.price_unit = line.product_id.list_price
        #     line.price_subtotal = float(line.price_unit) * float(line.product_uom_qty)
        #     if line.duration or line.product_price:
        #         line.price_unit = line.product_price * line.duration
        #         # price_unit = line.price_unit * line.duration
        #         line.price_subtotal = float(line.price_unit) * float(line.product_uom_qty)*(100-line.discount)/100
        #         line.amount_discount = (
        #                                line.product_uom_qty * line.price_unit) *(100-line.discount)/100
    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.order_id.currency_id,
            product=self.product_id,
            taxes=self.tax_id,
            price_unit=self.price_unit * self.duration if self.duration else  self.price_unit,
            quantity=self.product_uom_qty,
            discount=self.discount,
            price_subtotal=self.price_subtotal,
        )

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLineInheritTime, self)._prepare_invoice_line()
        res.update({'duration': self.duration,
                    'product_price': self.product_price,

                    })
        return res
class moveOrderLineInheritTime(models.Model):

    _inherit = "account.move.line"

    duration = fields.Float(string="المدة",default=1)
    product_price = fields.Float()
