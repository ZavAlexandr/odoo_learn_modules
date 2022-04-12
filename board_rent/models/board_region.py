from odoo import fields, models, _


class BoardRegion(models.Model):
    _name = 'board_rent.board_region'
    _description = _('Board regions')
    _rec_name = 'title'
    _order = 'title'

    title = fields.Char(string=_('Title'), required=True)
