# -*- coding: utf-8 -*-
{
    'name': "BonSens Lux Design Add-on",

    'summary': """
        Customization of Contacts, CRM and Rest API for BonSens
        """,

    'description': """
        Add-on for company 'Lux Design' by BonSens
    """,

    'author': "ZavAlex",
    'website': "https://www.bonsens.com.ua",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
