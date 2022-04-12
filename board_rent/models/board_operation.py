from odoo import fields, models, _, api


class BoardCategory(models.Model):
    _name = 'board_rent.board_operation'
    _description = _('Board operations')
    _rec_name = 'title'
    _order = 'title'

    title = fields.Char(string=_('Title'), required=True)
    price = fields.Float(string=_('Price'), digits=(15, 2))

    @api.onchange('price')
    def _onchange_price(self):
        for record in self:
            if record.price < 0:
                return {
                    'warning': {
                        'title': "Error",
                        'message': "Price cannot be negative!",
                    }
                }

