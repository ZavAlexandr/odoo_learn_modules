# -*- coding: utf-8 -*-
{
    'name': "REST API for BonSens (Lux Design)",

    'summary': """
        Data exchange with BonSens: Advertising enterprise management 2.3
        """,

    'description': """
        REST API for BonSens
    """,

    'author': "ZavAlex",
    'website': "https://www.bonsens.com.ua",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'bs_lux_design_add_on'],

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
