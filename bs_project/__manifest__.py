# -*- coding: utf-8 -*-
{
    'name': "bs_project",

    'summary': """
        Adds working hours/minutes in project
    """,

    'description': """
        Project add-on from BonSens
    """,

    'author': "ZavAlex",
    'website': "https://www.bonsens.com.ua",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
