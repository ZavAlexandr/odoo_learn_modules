# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class lead_form_for_site(models.Model):
#     _name = 'lead_form_for_site.lead_form_for_site'
#     _description = 'lead_form_for_site.lead_form_for_site'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
