from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    course_instructor = fields.Boolean(string=_("Course instructor"))
