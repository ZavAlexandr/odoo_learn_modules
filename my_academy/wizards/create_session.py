from odoo import fields, models, _


class CreateSessionWizard(models.TransientModel):
    _name = 'my_academy.create_session_wizard'
    _description = _('Create session wizard')

    def get_session(self):
        return self.env['my_academy.session'].browse(self._context.get('active_id'))

    session_ids = fields.Many2many('my_academy.session', string=_("Session"),
                                   required=True, default=get_session)
    attendants_ids = fields.Many2many('res.partner', string=_("Attendants"))

    def action_create_session(self):
        for rec_ses in self.session_ids:
            for rec_att in self.attendants_ids:
                new_rec = {
                    'session_id': rec_ses.id,
                    'partner_id': rec_att.id
                }
                self.env['my_academy.session.lines'].create(new_rec)
