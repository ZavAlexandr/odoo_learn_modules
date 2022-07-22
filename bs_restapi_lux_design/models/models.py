from odoo import models, api
import secrets

API_KEY_PARAMETER = 'bs_rest_api.apikey'


class bs_rest_api_parameter(models.Model):
    _inherit = "ir.config_parameter"

    @api.model
    def get_bs_apikey(self):
        apikey = self.env["ir.config_parameter"].sudo().get_param(API_KEY_PARAMETER)
        if apikey:
            return apikey

        apikey = secrets.token_urlsafe(40)
        self.env["ir.config_parameter"].sudo().set_param(API_KEY_PARAMETER, apikey)
        return apikey
