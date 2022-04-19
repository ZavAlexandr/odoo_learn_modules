# -*- coding: utf-8 -*-
{
    'name': "Lead form for site",
    'sequence': -90,

    'summary': """
        Get leads from site form
        """,

    'description': """
        Get leads from site form
    """,

    'author': "ZavAlex",
    'website': "http://bonsens.com.ua",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'templates/lead_form.xml',
        'templates/lead_form_ru.xml',
        'templates/lead_form_ua.xml',
        'templates/message.xml',
        'templates/message_ru.xml',
        'templates/message_ua.xml',
    ],
}
