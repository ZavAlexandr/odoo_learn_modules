from odoo import fields, models, _, api


class Board(models.Model):
    _name = 'board_rent.board'
    _description = _('Boards')
    _rec_name = 'title'
    _order = 'title'

    title = fields.Char(string=_('Title'), required=True)
    region_id = fields.Many2one(comodel_name='board_rent.board_region', string=_('Region'))
    type_id = fields.Many2one(comodel_name='board_rent.board_type', string=_('Type'))
    sides = fields.Integer(string=_('Sides'), required=True, default=1)
    price = fields.Float(string=_('Price'), digits=(15, 2))
    photo = fields.Image(string=_('Board photo'))
    comments = fields.Text(string=_('Comments'))
    rent_count = fields.Integer(string=_('Rent count'), compute='_compute_rent_count')

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

    def _compute_rent_count(self):
        for rec in self:
            rec.rent_count = self.env['board_rent.rent_order'].search_count([('board_id', '=', rec.id)])

    def open_orders_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rent orders for board',
            'res_model': 'board_rent.rent_order',
            'domain': [('board_id', '=', self.id)],
            'context': {'default_board_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',
        }
