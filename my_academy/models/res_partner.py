from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    course_instructor = fields.Boolean('Course instructor')
