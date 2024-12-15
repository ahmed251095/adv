from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    discount_method = fields.Selection([("fixed", "Fixed"), ("percentage", "Percentage")], string="Discount Method")
    discount_amount = fields.Float(string="Discount Amount")
    total_discount = fields.Float(string="- Discount", compute="_compute_total_discount")
    sale_order = fields.Boolean(string='Sale Order', compute='compute_sale_order', default=False)

    def compute_sale_order(self):
        for move_id in self:
            move_id.sale_order = False
            sale_id =move_id.invoice_line_ids.mapped('sale_line_ids').mapped('order_id')
            if sale_id:
                move_id.sale_order = True

    @api.onchange("discount_method", "discount_amount", "amount_untaxed")
    def onchange_on_total_discount(self):
        for rec in self:
            if rec.state == "draft":
                if rec.discount_amount and rec.discount_method:
                    if rec.amount_untaxed:
                        rec.total_discount = rec.count_total_discount()
                        rec.amount_total = (rec.amount_untaxed + rec.amount_tax) - rec.total_discount
                    else:
                        rec.total_discount = 0.0
                else:
                    rec.total_discount = 0.0

    @api.depends('line_ids.debit',
                 'line_ids.credit',
                 'line_ids.currency_id',
                 'line_ids.amount_currency',
                 'line_ids.amount_residual',
                 'line_ids.amount_residual_currency',
                 'line_ids.payment_id.state',
                 'total_discount')
    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()
        for rec in self:
            if rec.total_discount:
                rec.amount_total = rec.amount_total - rec.total_discount
                rec.amount_residual = rec.amount_total
            elif rec.discount_amount and rec.discount_method:
                total_discount = rec.count_total_discount()
                rec.amount_total = rec.amount_total - total_discount
                rec.amount_residual = rec.amount_total
        return res

    def count_total_discount(self):
        amount = 0
        for rec in self:
            if rec.discount_amount and rec.discount_method:
                if rec.discount_method == "fixed":
                    amount = rec.discount_amount
                else:
                    amount = round((rec.discount_amount * rec.amount_untaxed) / 100, 2)
        return amount

    @api.depends("discount_method", "discount_amount", "amount_untaxed")
    def _compute_total_discount(self):
        for rec in self:
            if rec.discount_amount and rec.discount_method:
                rec.total_discount = rec.count_total_discount()
            else:
                rec.total_discount = 0.0

    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        for rec in self:
            if rec.discount_method == 'fixed':
                if rec.discount_amount > rec.amount_total:
                    raise UserError(_('You can not add more then amount in fix rate'))
            if rec.discount_method == 'percentage':
                if rec.discount_amount > 100 or  rec.discount_amount < 0:
                    raise UserError(_('You can not add value less then 0 and grater then 100'))

        return res