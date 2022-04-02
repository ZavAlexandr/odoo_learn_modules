from odoo import fields, models, _


class SessionLines(models.Model):
    _name = 'my_academy.session.lines'
    _description = _('Our sessions lines')
    partner_id = fields.Many2one('res.partner', string=_('Attendant'))
    session_id = fields.Many2one('my_academy.session', string=_('Session ID'))
