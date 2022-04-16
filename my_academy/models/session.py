from datetime import date, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'my_academy.session'
    _description = _('Our sessions')
    _rec_name = 'ses_name'
    _inherit = ['mail.thread']

    ses_name = fields.Char(_('Session name'))
    start_date = fields.Date(string=_('Start date'), default=date.today())
    duration = fields.Integer(_('Duration'))
    seats = fields.Integer(_('Number of seats'))
    instructor_id = fields.Many2one(comodel_name='res.partner', string=_('Instructor'))
    course_id = fields.Many2one(comodel_name='my_academy.course', inverse_name='session_ids',
                                string=_('Course'), required=True)
    # attendant_lines_ids = fields.Many2many('my_academy.session.lines', string=_('Attendants'))
    attendant_lines_ids = fields.One2many('my_academy.session.lines', 'session_id',
                                          string=_('Attendants'))
    seats_taken_percent = fields.Float(string=_('Seats taken %'),
                                       compute='_compute_seats_taken_percent')
    end_date = fields.Date(string=_('End Date'), compute='_compute_end_date', store=True)
    is_active = fields.Boolean(string=_("Active"), default=True)

    @api.depends('seats', 'attendant_lines_ids')
    def _compute_seats_taken_percent(self):
        for record in self:
            if record.seats == 0:
                record.seats_taken_percent = 0
            else:
                count = 0
                for i in record.attendant_lines_ids:
                    count += 1
                record.seats_taken_percent = count / record.seats * 100

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if not rec.duration:
                rec.end_date = rec.start_date
            else:
                rec.end_date = rec.start_date + timedelta(days=rec.duration)

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
