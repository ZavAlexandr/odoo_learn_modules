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


def get_language(req_lang):
    lang = 'uk_UA'

    if req_lang:
        if req_lang.lower() == 'ru':
            lang = 'ru_RU'
        elif req_lang.lower() == 'ua':
            lang = 'uk_UA'
        else:
            lang = 'en_US'

    return lang


class bs_rest_api(http.Controller):

    @http.route('/api/get_contacts', auth='public', method=['GET'], csrf=False)
    def get_contacts(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        write_time = kw.get('write_time')
        write_date = kw.get('write_date')
        if write_time or write_date:
            if write_time:
                date_time_obj = datetime.strptime(write_time, '%d.%m.%Y-%H:%M:%S')
            else:
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
        fields_list = ['name', 'company_type', 'email', 'phone', 'vat', 'comment', 'parent_id']
        for fld in fields_list:
            val = kw.get(fld)
            if not val:
                if fld == 'company_type':
                    val = 'company'
                else:
                    val = ''
            else:
                if fld == 'parent_id':
                    val = int(val)

            new_rec.update({fld: val})

        created_id = request.env['res.partner'].sudo().create(new_rec)

        output = get_json_ok_response(200, created_id.id)
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
        fields_list = ['name', 'company_type', 'email', 'phone', 'vat', 'comment', 'parent_id']
        for fld in fields_list:
            val = kw.get(fld)
            if val:
                if fld == 'parent_id':
                    val = int(val)

            edit_rec.update({fld: val})

        is_updated = data.sudo().write(edit_rec)

        if is_updated:
            output = get_json_ok_response(200, 'Record updated for res.partner with ID: ' + str(partner_id))
        else:
            output = get_json_error_response(504, 'Error updating record for res.partner with ID: ' + str(partner_id))
        return json.dumps(output)

    @http.route('/api/get_crm_lost_reasons', auth='public', method=['GET'], csrf=False)
    def get_crm_lost_reasons(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        lang = get_language(kw.get('lang'))
        data_list = []

        all_data = request.env['crm.lost.reason'].sudo().with_context(lang=lang).search([])
        for rec in all_data:
            data = dict()
            data['id'] = rec.id
            data['name'] = rec.name
            data['write_date'] = rec.write_date
            data_list.append(data)

        json_data = json.dumps(data_list, default=date_utils.json_default)
        return Response(json_data, 200)

    @http.route('/api/get_crm_stages', auth='public', method=['GET'], csrf=False)
    def get_crm_stages(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        lang = get_language(kw.get('lang'))
        data_list = []

        all_data = request.env['crm.stage'].sudo().with_context(lang=lang).search([], order='sequence asc')
        for rec in all_data:
            data = dict()
            data['id'] = rec.id
            data['name'] = rec.name
            data['is_won'] = rec.is_won
            data['write_date'] = rec.write_date
            data_list.append(data)

        json_data = json.dumps(data_list, default=date_utils.json_default)
        return Response(json_data, 200)

    @http.route('/api/get_odoo_users', auth='public', method=['GET'], csrf=False)
    def get_odoo_users(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        data_list = []

        all_data = request.env['res.users'].sudo().search([('share', '=', False)])
        for rec in all_data:
            data = dict()
            data['id'] = rec.id
            data['name'] = rec.name
            data['write_date'] = rec.write_date
            data_list.append(data)

        json_data = json.dumps(data_list, default=date_utils.json_default)
        return Response(json_data, 200)

    @http.route('/api/get_utm_sources', auth='public', method=['GET'], csrf=False)
    def get_users(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        lang = get_language(kw.get('lang'))
        data_list = []

        all_data = request.env['utm.source'].sudo().with_context(lang=lang).search([])
        for rec in all_data:
            data = dict()
            data['id'] = rec.id
            data['name'] = rec.name
            data['write_date'] = rec.write_date
            data_list.append(data)

        json_data = json.dumps(data_list, default=date_utils.json_default)
        return Response(json_data, 200)

    @http.route('/api/get_leads', auth='public', method=['GET'], csrf=False)
    def get_leads(self, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        data_list = []

        domain = [
            ('type', '=', 'opportunity'),
        ]

        write_date = kw.get('write_date')
        write_time = kw.get('write_time')
        if write_time or write_date:
            if write_time:
                date_time_obj = datetime.strptime(write_time, '%d.%m.%Y-%H:%M:%S')
            else:
                date_time_obj = datetime.strptime(write_date, '%d.%m.%Y')

            domain += [('write_date', '>=', date_time_obj)]



        stage = kw.get('stage')
        if stage:
            domain += [('stage_id', '=', int(stage))]

        lang = get_language(kw.get('lang'))

        all_data = request.env['crm.lead'].sudo().with_context(lang=lang, active_test=False).search(domain)

        for rec in all_data:
            data = dict()
            data['id'] = rec.id
            data['name'] = rec.name
            data['partner_id'] = correct_field_data(rec.partner_id.id)
            data['expected_revenue'] = rec.expected_revenue
            data['description'] = correct_field_data(rec.description)
            data['source_id'] = correct_field_data(rec.source_id.id)
            data['stage_id'] = correct_field_data(rec.stage_id.id)
            data['user_id'] = correct_field_data(rec.user_id.id)
            data['lost_reason'] = correct_field_data(rec.lost_reason.id)
            data['active'] = rec.active
            data['write_date'] = rec.write_date
            data_list.append(data)

        json_data = json.dumps(data_list, default=date_utils.json_default)
        return Response(json_data, 200)

    @http.route('/api/update_lead/<int:lead_id>', auth='public', method=['GET'], csrf=False)
    def update_lead(self, lead_id, **kw):
        req_apikey = kw.get('apikey')
        res = check_apikey(req_apikey)
        if isinstance(res, str):
            return res

        data = request.env['crm.lead'].sudo().with_context(active_test=False).search([('id', '=', lead_id)])
        if not data:
            output = get_json_error_response(505, 'No lead with ID: ' + str(lead_id))
            return json.dumps(output)

        edit_rec = {}
        fields_list = ['expected_revenue', 'stage_id', 'user_id', 'name', 'description', 'archived', 'lost_reason']
        set_archive_to = False

        for fld in fields_list:
            val = kw.get(fld)
            if val:
                if fld == 'expected_revenue':
                    edit_rec.update({fld: float(val)})
                elif fld == 'archived':
                    if val.lower() == 'true':
                        set_archive_to = True
                    else:
                        set_archive_to = False
                elif fld == 'stage_id' or fld == 'user_id' or fld == 'lost_reason':
                    edit_rec.update({fld: int(val)})
                else:
                    edit_rec.update({fld: val})

        if set_archive_to and data.active:
            data.action_archive()
        elif not set_archive_to and not data.active:
            data.action_unarchive()

        is_updated = data.sudo().write(edit_rec)

        if is_updated:
            output = get_json_ok_response(200, 'Record updated for crm.lead with ID: ' + str(lead_id))
        else:
            output = get_json_error_response(506, 'Error updating record for crm.lead with ID: ' + str(lead_id))
        return json.dumps(output)
