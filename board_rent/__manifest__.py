# -*- coding: utf-8 -*-
{
    'name': "Board rent",
    'sequence': -101,

    'summary': """
        Advertising media rental accounting
        """,

    'description': """
        Simple advertising media rental accounting module
    """,

    'author': "ZavAlex",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],
    'application': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/board_category_views.xml',
        'views/board_region_views.xml',
        'views/board_types_views.xml',
        'views/board_operation_views.xml',
        'views/board_views.xml',
        'views/rent_order_views.xml',
        'views/board_rent_menus.xml',
        'views/templates.xml',
        'data/board_rent_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
