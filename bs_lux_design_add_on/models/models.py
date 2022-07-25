# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


def bs_get_formatted_phone(number, bs_phone_format):
    if not bs_phone_format:
        return number

    new_number = number

    if bs_phone_format == 'type_1':
        if len(number) == 10:
            new_number = '+38{}'.format(number)
        elif len(number) == 9:
            new_number = '+380{}'.format(number)
        elif len(number) == 12 and number[:3] == '380':
            new_number = '+{}'.format(number)

    if bs_phone_format == 'type_2':
        if len(number) == 10:
            new_number = '38{}'.format(number)
        elif len(number) == 9:
            new_number = '380{}'.format(number)

    return new_number


def bs_check_phone(number, bs_phone_format):
    if not bs_phone_format:
        return True

    if bs_phone_format == 'type_1':
        if len(number) == 13:
            return True
        else:
            return False

    if bs_phone_format == 'type_2':
        if len(number) == 12:
            return True
        else:
            return False

    if bs_phone_format == 'type_3':
        if len(number) == 10:
            return True
        else:
            return False


class bs_contacts_lux_design(models.Model):
    _inherit = 'res.partner'

    main_contact_id = fields.Many2one('res.partner', _('Main contact'))
    is_child_contact = fields.Boolean(_('Is child contact'))

    @api.onchange('main_contact_id')
    def _onchange_main_contact(self):
        self.ensure_one()
        if self.main_contact_id:
            self.is_child_contact = True
        else:
            self.is_child_contact = False

    @api.onchange('phone')
    def _onchange_phone(self):
        self.ensure_one()
        bs_phone_format = self.env.company.bs_phone_format

        for obj in self:
            if obj.phone:
                new_number = bs_get_formatted_phone(obj.phone, bs_phone_format)
                if obj.phone != new_number:
                    obj.phone = new_number

    @api.onchange('mobile')
    def _onchange_mobile(self):
        self.ensure_one()
        bs_phone_format = self.env.company.bs_phone_format

        for obj in self:
            if obj.mobile:
                new_number = bs_get_formatted_phone(obj.mobile, bs_phone_format)
                if obj.mobile != new_number:
                    obj.mobile = new_number

    @api.constrains('phone', 'mobile')
    def _check_number_format(self):
        self.ensure_one()
        bs_phone_format = self.env.company.bs_phone_format

        if self.phone:
            if not bs_check_phone(self.phone, bs_phone_format):
                raise ValidationError(_('Check phone length!'))

        if self.mobile:
            if not bs_check_phone(self.mobile, bs_phone_format):
                raise ValidationError(_('Check mobile length!'))


class bs_crm_lead_lux_design(models.Model):
    _inherit = 'crm.lead'

    is_child_contact = fields.Boolean(_('Is child contact'))

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.ensure_one()
        self.is_child_contact = self.partner_id.is_child_contact

        if self.is_child_contact:
            return {
                'warning': {
                    'title': _('Warning!'),
                    'message': _('You have selected contact - child of: "') + self.partner_id.main_contact_id.name +
                               '"! ' + _('Click on "Set to main contact" in button bar for selecting main contact.')}
            }

    def set_main_contact(self):
        self.partner_id = self.partner_id.main_contact_id
        self.is_child_contact = False

    @api.onchange('phone')
    def _onchange_phone(self):
        self.ensure_one()
        bs_phone_format = self.env.company.bs_phone_format

        for obj in self:
            if obj.phone:
                new_number = bs_get_formatted_phone(obj.phone, bs_phone_format)
                if obj.phone != new_number:
                    obj.phone = new_number


class bs_res_company_lux_design(models.Model):
    _inherit = 'res.company'

    bs_phone_format = fields.Selection(
        [('type_1', '+38067'), ('type_2', '38067'), ('type_3', '067')],
        string=_('Phone format'))


class bs_crm_stage_lux_design(models.Model):
    _inherit = 'crm.stage'

    export_to_bonsens = fields.Boolean(_('Export to BonSens'),
                                       help=_('Contacts in this stage will be exported to BonSens'))
