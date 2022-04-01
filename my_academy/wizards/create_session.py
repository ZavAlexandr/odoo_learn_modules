from odoo import models, fields, api


class CreateSessionWizard(models.TransientModel):
    _name = 'my_academy.create_session_wizard'
    _description = 'Create session wizard'

    def get_session(self):
        return self.env['my_academy.session'].browse(self._context.get('active_id'))

    session = fields.Many2many('my_academy.session',
                               string="Session", required=True, default=get_session)
    attendants = fields.Many2many('res.partner', string="Attendants")

    def action_create_session(self):
        for rec_ses in self.session:
            for rec_att in self.attendants:
                newrec = {
                    'session_id': rec_ses.id,
                    'partner_id': rec_att.id
                }
                self.env['my_academy.session.lines'].create(newrec)

