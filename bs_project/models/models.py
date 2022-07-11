# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class bs_project(models.Model):
    _inherit = 'project.project'

    work_hours = fields.Integer(_('Hours'))
    work_minutes = fields.Integer(_('Minutes'))

    @api.onchange('work_hours')
    def _onchange_work_hours(self):
        for rec in self:
            rec.work_minutes = rec.work_hours * 60

    @api.onchange('work_minutes')
    def _onchange_work_minutes(self):
        for rec in self:
            rec.work_hours = round(rec.work_minutes / 60)
