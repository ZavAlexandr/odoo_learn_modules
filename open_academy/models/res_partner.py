from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'
    instructor = fields.Boolean('Instructor')
