from odoo import models, fields


class SessionLines(models.Model):
    _name = 'my_academy.session.lines'
    _description = 'Our sessions lines'
    partner_id = fields.Many2one('res.partner', string='Attendant')
    session_id = fields.Many2one('my_academy.session', string='Session ID')
