from odoo import fields, models, _


class BoardType(models.Model):
    _name = 'board_rent.board_type'
    _description = _('Board types')
    _rec_name = 'title'
    _order = 'title'

    title = fields.Char(string=_('Title'), required=True)


# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class board_rent(models.Model):
#     _name = 'board_rent.board_rent'
#     _description = 'board_rent.board_rent'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
