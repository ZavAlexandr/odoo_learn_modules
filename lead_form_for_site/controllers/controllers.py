from odoo import http, _
from odoo.http import request


class LeadFormSiteController(http.Controller):
    @http.route('/get_lead_form', auth='public', method=['GET'])
    def get_lead_form(self, **kw):
        response = http.request.render('lead_form_for_site.lead_form', {})
        return response

    @http.route('/get_lead_form_ru', auth='public', method=['GET'])
    def get_lead_form_ru(self, **kw):
        response = http.request.render('lead_form_for_site.lead_form_ru', {})
        return response

    @http.route('/get_lead_form_ua', auth='public', method=['GET'])
    def get_lead_form_ua(self, **kw):
        response = http.request.render('lead_form_for_site.lead_form_ua', {})
        return response

    @http.route('/add_new_lead', auth='public', method=['POST'], csrf=False)
    def add_new_lead(self, **kw):

        client_name = kw.get('client_name')
        if client_name is None:
            client_name = _('Client from site')

        client_email = kw.get('client_email')
        if client_email is None:
            client_email = ''

        client_phone = kw.get('client_phone')
        if client_phone is None:
            client_phone = ''

        subject = kw.get('subject')
        if subject is None:
            subject = ''

        new_rec = {
            'name': subject,
            'type': 'lead',
            'partner_name': client_name,
            'email_from': client_email,
            'phone': client_phone,
        }
        request.env['crm.lead'].sudo().create(new_rec)

        template = 'lead_form_for_site.message'

        lang = kw.get('lang')
        if lang == 'ru':
            template = 'lead_form_for_site.message_ru'
        elif lang == 'ua':
            template = 'lead_form_for_site.message_ua'

        response = http.request.render(template, {})
        return response

