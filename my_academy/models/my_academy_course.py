from odoo import models, fields, _


class Course(models.Model):
    _name = 'my_academy.course'
    _description = 'Our courses'
    _rec_name = 'title'

    title = fields.Char(string='Title', required=True)
    coursedesc = fields.Char(string='Description')
    responsible_id = fields.Many2one(comodel_name='res.users', string='Responsible user')
    session_ids = fields.One2many(comodel_name='my_academy.session', string='Session', required=False,
                                  inverse_name="course_id")

    _sql_constraints = [
          ('check_NameDescription', 'check(title != coursedesc)',
           _("Title must not equal description! Error!")),
          ('check_Name','unique(title)',
           _("Title of the course must be unique! Error!")),]

    def copy(self, default={}):
        default['title'] = 'Copy of ' + self.title
        ret = super(Course, self).copy(default=default)
        return ret
