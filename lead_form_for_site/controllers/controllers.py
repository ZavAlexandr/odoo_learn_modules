from odoo import http, _
from odoo.http import request


class LeadFormSiteController(http.Controller):

    @http.route('/get_lead_form', auth='public', methods=['GET'])
    @http.route('/<string:lang>/get_lead_form', auth='public', methods=['GET'])
    def get_lead_form(self, **kw):
        lang = kw.get('lang')

        lang_template = 'lead_form'
        if lang == 'ru':
            lang_template = 'lead_form_ru'
        elif lang == 'ua':
            lang_template = 'lead_form_ua'

        response = http.request.render('lead_form_for_site.' + lang_template, {})
        # response.headers['X-Frame-Options'] = 'ALLOW-FROM ' + http.request.httprequest.host_url
        return response

    @http.route('/add_new_lead', auth='public', methods=['POST'], csrf=False)
    def add_new_lead(self, **kw):

        fields_dic = {
            'subject': 'name',
            'client_name': 'partner_name',
            'client_email': 'email_from',
            'client_phone': 'phone'
        }

        new_rec = {}
        for key_request, key_record in fields_dic.items():
            val_request = kw.get(key_request)

            if not val_request:
                if key_request == 'client_name':
                    val_request = _('Client from site')
                else:
                    val_request = ''

            new_rec.update({key_record: val_request})

        campaign_id = kw.get('campaign')
        if campaign_id:
            campaign_record = request.env['utm.campaign'].sudo().search([('id', '=', int(campaign_id))])
            if campaign_record:
                new_rec.update({'campaign_id': int(campaign_id)})

        source_id = kw.get('source')
        if source_id:
            source_record = request.env['utm.source'].sudo().search([('id', '=', int(source_id))])
            if source_record:
                new_rec.update({'source_id': int(source_id)})

        new_rec.update({'type': 'lead'})
        request.env['crm.lead'].sudo().create(new_rec)

        template = 'lead_form_for_site.message'

        lang = kw.get('lang')
        if lang == 'ru':
            template = 'lead_form_for_site.message_ru'
        elif lang == 'ua':
            template = 'lead_form_for_site.message_ua'

        response = http.request.render(template, {})
        return response
