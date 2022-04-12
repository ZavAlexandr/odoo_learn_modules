from odoo import api, fields, models, _


class RentOrderWorks(models.Model):
    _name = 'board_rent.rent_order_works'
    _description = 'Rent order works'
    order_id = fields.Many2one('board_rent.rent_order', string='Order ID')
    operation_id = fields.Many2one('board_rent.board_operation', string='Operation')
    description = fields.Char(string=_('Description'))
    price = fields.Float(string=_('Price'), digits=(15, 2))
    amount = fields.Float(string=_('Amount'), digits=(15, 3))
    sum = fields.Float(string=_('Sum'), digits=(15, 2))

    @api.onchange('operation_id')
    def _onchange_operation_id(self):
        self.ensure_one()
        self.price = self.operation_id.price

    @api.onchange('amount')
    def _onchange_amount(self):
        self.ensure_one()
        self.sum = self.price * self.amount

