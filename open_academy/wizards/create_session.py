from odoo import models, fields, api


class CreateSessionWizard(models.TransientModel):
    _name = 'create.session.wizard'
    _description = 'Create session wizard'

    def get_session(self):
        return self.env['open_academy.session'].browse(self._context.get('active_id'))

    session = fields.Many2many('open_academy.session',
                               string="Session", required=True, default=get_session)
    attendants = fields.Many2many('res.partner', string="Attendants")

    def action_create_session(self):
        for rec_ses in self.session:
            for rec_att in self.attendants:
                newrec = {
                    'session_id': rec_ses.id,
                    'partner_id': rec_att.id
                }
                self.env['open_academy.session.lines'].create(newrec)

