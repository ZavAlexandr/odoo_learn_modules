import json
from datetime import datetime
from odoo import http
from odoo.http import request, Response
from odoo.tools import date_utils


def get_json_error_response(code, message):
    output = {
        'error': {
            'code': code,
            'message': message
        }
    }
    return output


def get_json_ok_response(code, message):
    output = {
        'ok': {
            'code': code,
            'message': message
        }
    }
    return output


def check_apikey(req_apikey):

    if not req_apikey:
        output = get_json_error_response(501, 'No API key in request')
        return json.dumps(output)

    params = request.env["ir.config_parameter"]
    app_apikey = params.get_bs_apikey()

    if req_apikey != app_apikey:
        output = get_json_error_response(502, 'Wrong API key')
        return json.dumps(output)

    return True


def correct_field_data(var):
    if not var:
        var = ''

    return var


def get_contact_data(records):
    data_list = []

    for rec in records:
        data = dict()
        data['id'] = rec.id
        data['parent_id'] = correct_field_data(rec.parent_id.id)
        data['company_type'] = rec.company_type
        data['name'] = rec.name
        data['comment'] = correct_field_data(rec.comment).strip()
        data['email'] = correct_field_data(rec.email)
        data['phone'] = correct_field_data(rec.phone)
        data['vat'] = correct_field_data(rec.vat)
        data['write_date'] = rec.write_date
        data_list.append(data)

    json_data = json.dumps(data_list, default=date_utils.json_default)
    return Response(json_data, 200)


class bs_rest_api(http.Controller):

    @http.route('/api/get_contacts', auth='public', method=['GET'], csrf=False)
    def get_contacts(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        write_date = kw.get('write_date')
        if write_date:
            date_time_obj = datetime.strptime(write_date, '%d.%m.%Y')
            all_data = request.env['res.partner'].sudo().search([('write_date', '>=', date_time_obj)])
        else:
            all_data = request.env['res.partner'].sudo().search([])

        return get_contact_data(all_data)

    @http.route('/api/get_contact/<int:partner_id>', auth='public', method=['GET'], csrf=False)
    def get_contact(self, partner_id, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        data = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
        return get_contact_data(data)

    @http.route('/api/add_contact', auth='public', method=['GET'], csrf=False)
    def add_contact(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        new_rec = {}
        fields_list = ['name', 'company_type', 'email', 'phone', 'vat', 'comment']
        for fld in fields_list:
            val = kw.get(fld)
            if not val:
                if fld == 'company_type':
                    val = 'company'
                else:
                    val = ''
            new_rec.update({fld: val})

        created_id = request.env['res.partner'].sudo().create(new_rec)

        output = get_json_error_response(200, created_id.id)
        return json.dumps(output)

    @http.route('/api/update_contact/<int:partner_id>', auth='public', method=['GET'], csrf=False)
    def update_contact(self, partner_id, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        data = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
        if not data:
            output = get_json_error_response(503, 'No contact for ID: ' + str(partner_id))
            return json.dumps(output)

        edit_rec = {}
        fields_list = ['name', 'company_type', 'email', 'phone', 'vat', 'comment']
        for fld in fields_list:
            val = kw.get(fld)
            if val:
                edit_rec.update({fld: val})

        is_updated = data.sudo().write(edit_rec)

        if is_updated:
            output = get_json_ok_response(200, 'Record updated for res.partner with ID: ' + str(partner_id))
        else:
            output = get_json_error_response(504, 'Error updating record for ID: ' + str(partner_id))
        return json.dumps(output)
