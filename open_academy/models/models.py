from odoo import models, fields, api, _
from datetime import date, timedelta
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Our courses'
    title = fields.Char('Title')
    coursedesc = fields.Char('Description')
    responsible = fields.Many2one('res.users', string='Responsible user')

    _sql_constraints = [
          ('check_NameDescription', 'check(title != coursedesc)',
           _("Title must not equal description! Error!")),
          ('check_Name','unique(title)',
           _("Title of the course must be unique! Error!")),]

    def copy(self, default={}):
        default['title'] = 'Copy of '+self.title
        ret = super(Course, self).copy(default=default)
        return ret


class Session(models.Model):
    _name = 'open_academy.session'
    _description = 'Our sessions'
    ses_name = fields.Char('Session name')
    startdate = fields.Date('Start date', default=date.today())
    duration = fields.Integer('Duration')
    seats = fields.Integer('Number of seats')
    instructor_id = fields.Many2one('res.partner', string='Instructor')
    course_id = fields.Many2one('open_academy.course', string='Course', required=True)
    #attendant_lines_ids = fields.Many2many('open_academy.session.lines', string='Attendants')
    attendant_lines_ids = fields.One2many('open_academy.session.lines', 'session_id', string='Attendants')
    seats_taken_percent = fields.Float('Seats taken %', compute='_compute_seatstaken')
    enddate = fields.Date('End Date', compute='_compute_enddate', store=True)
    is_active = fields.Boolean(string="Active", default=True)

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
                    'title': "Error",
                    'message': "Seats cannot be negative!",
                    }
                }


    @api.onchange('attendant_lines_ids')
    def _onchange_attendant_lines_ids(self):
        for record in self:
            if len(record.attendant_lines_ids) > record.seats:
                return {
                    'warning': {
                    'title': "Error",
                    'message': "All seats taken!",
                    }
                }

    @api.constrains('attendant_lines_ids')
    def _constrains_attendant_lines_ids(self):
        for record in self:
            for line in record.attendant_lines_ids:
                if record.instructor_id == line.partner_id:
                    raise ValidationError("Attendant cannot be the same as instructor!")


    @api.depends('startdate', 'duration')
    def _compute_enddate(self):
        for rec in self:
            if not rec.duration:
                rec.enddate = rec.startdate
            else:
                rec.enddate = rec.startdate + timedelta(days=rec.duration)


class SessionLines(models.Model):
    _name = 'open_academy.session.lines'
    _description = 'Our sessions lines'
    partner_id = fields.Many2one('res.partner', string='Attendant')
    session_id = fields.Many2one('open_academy.session', string='Session ID')

