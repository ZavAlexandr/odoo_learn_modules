from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'my_academy.session'
    _description = _('Our sessions')
    _rec_name = 'ses_name'

    ses_name = fields.Char(_('Session name'))
    startdate = fields.Date(string=_('Start date'), default=date.today())
    duration = fields.Integer(_('Duration'))
    seats = fields.Integer(_('Number of seats'))
    instructor_id = fields.Many2one(comodel_name='res.partner', string=_('Instructor'))
    course_id = fields.Many2one(comodel_name='my_academy.course', inverse_name='session_ids',
                                string=_('Course'), required=True)
    # attendant_lines_ids = fields.Many2many('my_academy.session.lines', string=_('Attendants'))
    attendant_lines_ids = fields.One2many('my_academy.session.lines', 'session_id', string=_('Attendants'))
    seats_taken_percent = fields.Float(string=_('Seats taken %'), compute='_compute_seatstaken')
    enddate = fields.Date(string=_('End Date'), compute='_compute_enddate', store=True)
    is_active = fields.Boolean(string=_("Active"), default=True)

    @api.depends('seats', 'attendant_lines_ids')
    def _compute_seatstaken(self):
        for record in self:
            if record.seats == 0:
                record.seats_taken_percent = 0
            else:
                count = 0
                for i in record.attendant_lines_ids:
                    count += 1
                record.seats_taken_percent = count / record.seats * 100

    @api.onchange('seats')
    def _onchange_seats(self):
        for record in self:
            if record.seats < 0:
                return {
                    'warning': {
                        'title': _("Error"),
                        'message': _("Seats cannot be negative!"),
                    }
                }

    @api.onchange('attendant_lines_ids')
    def _onchange_attendant_lines_ids(self):
        for record in self:
            if len(record.attendant_lines_ids) > record.seats:
                return {
                    'warning': {
                        'title': _("Error"),
                        'message': _("All seats taken!"),
                    }
                }

    @api.constrains('attendant_lines_ids')
    def _constrains_attendant_lines_ids(self):
        for record in self:
            for line in record.attendant_lines_ids:
                if record.instructor_id == line.partner_id:
                    raise ValidationError(_("Attendant cannot be the same as instructor!"))

    @api.depends('startdate', 'duration')
    def _compute_enddate(self):
        for rec in self:
            if not rec.duration:
                rec.enddate = rec.startdate
            else:
                rec.enddate = rec.startdate + timedelta(days=rec.duration)
