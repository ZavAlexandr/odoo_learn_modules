from odoo import fields, models, _


class BoardCategory(models.Model):
    _name = 'board_rent.board_category'
    _description = _('Board categories')
    _rec_name = 'title'
    _order = 'title'

    title = fields.Char(string=_('Title'), required=True)
