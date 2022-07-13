# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class bs_project(models.Model):
    _inherit = 'project.project'

    bs_time_limit = fields.Float(_('Time limit (h:m)'))
    bs_time_remain = fields.Float(_('Remain time (h:m)'), compute='_compute_remain_time')

    def _compute_remain_time(self):
        for doc in self:
            if doc.bs_time_limit == 0:
                doc.bs_time_remain = 0
                return

            unit_amount = 0
            data = self.env['account.analytic.line'].sudo().with_context().search([('project_id', '=', doc.id)])
            for rec in data:
                unit_amount += rec.unit_amount

            doc.bs_time_remain = doc.bs_time_limit - unit_amount
