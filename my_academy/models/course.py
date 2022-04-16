from odoo import fields, models, _


class Course(models.Model):
    _name = 'my_academy.course'
    _description = _('Our courses')
    _rec_name = 'title'

    title = fields.Char(string=_('Title'), required=True)
    course_desc = fields.Char(_('Description'))
    responsible_id = fields.Many2one(comodel_name='res.users', string=_('Responsible user'))
    session_ids = fields.One2many(comodel_name='my_academy.session', inverse_name='course_id',
                                  string=_('Session'), required=False)

    _sql_constraints = [
          ('check_NameDescription', 'check(title != coursedesc)',
           _("Title must not equal description! Error!")),
          ('check_Name', 'unique(title)',
           _("Title of the course must be unique! Error!")), ]

    def copy(self, default={}):
        default['title'] = _('Copy of ') + self.title
        ret = super(Course, self).copy(default=default)
        return ret
