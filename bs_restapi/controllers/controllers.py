from odoo import http
from odoo.http import request, Response
import json

from odoo.tools import date_utils


class bs_rest_api(http.Controller):

    @http.route('/api/get_contact', auth='public', method=['GET'], csrf=False)
    def get_contact(self, **kw):

        req_apikey = kw.get('apikey')
        if not req_apikey:
            output = {
                'results': {
                    'code': 200,
                    'message': 'No API key'
                }
            }
            return json.dumps(output)

        params = request.env["ir.config_parameter"]
        app_apikey = params.get_bs_apikey()

        if req_apikey != app_apikey:
            output = {
                'results': {
                    'code': 200,
                    'message': 'Wrong API key'
                }
            }
            return json.dumps(output)

        contact_id = kw.get('id')
        if contact_id:
            all_data = request.env['res.partner'].search(['id', '=', contact_id])
        else:
            all_data = request.env['res.partner'].search([])

        data_list = []
        for rec in all_data:
            data = dict()
            data['partner_id'] = rec.id
            data['company_type'] = rec.company_type
            data['name'] = rec.name
            data['email'] = rec.email
            data['phone'] = rec.phone
            data['vat'] = rec.vat
            data_list.append(data)

        json_data = json.dumps(data_list, default=date_utils.json_default)
        return Response(json_data, 200)
