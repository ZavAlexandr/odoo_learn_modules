from odoo import models, fields, api
import requests


class NPCargoTrackingWizard(models.TransientModel):
    _name = 'npcargotracking.wizard'
    _description = 'Nova Poshta cargo tracking wizard'

    cargo_number = fields.Char('Cargo number')
    track_result = fields.Html('Track result')

    def action_track_cargo(self):
        title = "Nova poshta tracking"
        message = self.np_track()

        self.track_result = message

        if message[0] == '#':
            msg_status = 'danger'
        else:
            msg_status = 'success'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': True,
                'type': msg_status,
            }
        }

    def np_track(self):
        api_key = '8f21966c593857f27ba4e22aae668910'
        url = "http://api.novaposhta.ua/v2.0/json/"
        headers = {'Content-type': 'text/json'}
        data = '''{
            "apiKey": "[APIKey]",
            "modelName": "TrackingDocument",
            "calledMethod": "getStatusDocuments",
            "methodProperties": {
                "Documents": [
                    {
                        "DocumentNumber": "[DocNumber]",
                        "Phone": "[Phone]"
                    }
                ]
            }
        }'''

        data = data.replace('[APIKey]', api_key)
        data = data.replace('[DocNumber]', self.cargo_number)
        data = data.replace('[Phone]', '')

        show_dict = {'DocumentCost': 'Стоимость',
                     'CitySender': 'Город отправителя',
                     'WarehouseSender': 'Отделение отправителя',
                     'CityRecipient': 'Город получателя',
                     'WarehouseRecipient': 'Отделение получателя',
                     'Status': 'Статус',
                     'ScheduledDeliveryDate': 'Плановая дата доставки',
                     'RecipientDateTime': 'Дата фактического получения'}

        res = requests.get(url, headers=headers, data=data)

        if res.status_code != 200:
            return '# Site error!'
        else:
            site_json = res.json()

            if not site_json.get('success'):
                return '#' + site_json['errors'][0]

            res_data = site_json['data']
            data_dict = res_data[0]

            np_info = ''
            for key, value in data_dict.items():
                show_dict_value = show_dict.get(key)
                if show_dict_value is not None:
                    np_info = np_info + '<p><b>' + show_dict_value + '</b>: ' + value + '</p>\n'

            return np_info


    @api.onchange('cargo_number')
    def _onchange_cargo_number(self):
        if not self.cargo_number == False:
            self.track_result = self.np_track()

    # cargo_num = '20450498147921'