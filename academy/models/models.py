from odoo import models, fields, api


class Teachers(models.Model):
    _name = 'academy.teachers'
    _description = 'Teachers'

    name = fields.Char(string="Name")
    #biography = fields.Html()
    biography = fields.Char(string="Biography")
    #course_ids = fields.One2many('academy.courses', 'teacher_id', string="Courses")
    course_ids = fields.One2many('product.template', 'teacher_id', string="Courses")


class Courses(models.Model):
    #_name = 'academy.courses'
    #_description = 'Courses'
    #_inherit = 'mail.thread'
    _inherit = 'product.template'

    name = fields.Char(string="Name")
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")

