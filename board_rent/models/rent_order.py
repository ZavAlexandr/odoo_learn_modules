from datetime import date
from odoo import api, fields, models, _


def diff_dates(date_1, date_2):
    if not date_1 or not date_2:
        return 0
    else:
        return abs(date_2 - date_1).days


class RentOrder(models.Model):
    _name = 'board_rent.rent_order'
    _description = _('Rent order')
    _rec_name = 'name'
    _order = 'doc_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Document number', copy=False, readonly=True, default=lambda x: _('New'))
    doc_date = fields.Date(string=_('Document date'), default=date.today())
    client_id = fields.Many2one(comodel_name='res.partner', string=_('Client'))
    board_id = fields.Many2one(comodel_name='board_rent.board', string=_('Board'))
    category_id = fields.Many2one(comodel_name='board_rent.board_category', string=_('Category'))
    start_date = fields.Date(string=_('Start date'))
    end_date = fields.Date(string=_('End date'))
    price = fields.Float(string=_('Price'), digits=(15, 2))
    discount_percent = fields.Float(string=_('Discount %'), digits=(10, 2))
    sum = fields.Float(string=_('Sum'), digits=(15, 2), compute='_compute_sum', store=True)
    works_ids = fields.One2many('board_rent.rent_order_works', 'order_id', string='Works')
    photo = fields.Image(string=_('Photo report'))
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                             ('done', 'Done'), ('cancel', 'Cancelled')], default='draft',
                             string=_("Status"), tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('board_rent.rent_order') or _('New')
        return super(RentOrder, self).create(vals)

    @api.onchange('board_id')
    def _onchange_board_id(self):
        self.ensure_one()
        self.price = self.board_id.price

    @api.depends('start_date', 'end_date', 'price', 'works_ids', 'discount_percent')
    def _compute_sum(self):
        for rec in self:
            operation_sum = 0
            for work in rec.works_ids:
                operation_sum += work.sum

            days_in_period = diff_dates(rec.start_date, rec.end_date)
            if days_in_period == 0:
                sum_rent = 0
            else:
                sum_rent = rec.price / 30 * days_in_period

            rec.sum = operation_sum + sum_rent

            if rec.discount_percent != 0:
                rec.sum = rec.sum - (rec.sum * rec.discount_percent / 100)
