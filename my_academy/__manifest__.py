# -*- coding: utf-8 -*-
{
    'name': "My academy",
    'sequence': -100,

    'summary': """
        Odoo learning module for Academy
    """,

    'description': """
        This module allows you to keep track of courses and sessions
    """,

    'author': "ZavAlex",
    'website': "http://www.zavalex.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'board'],
    'application': True,

    # always loaded
    'data': [
        'security/my_academy_groups.xml',
        'security/my_academy_security.xml',
        'security/ir.model.access.csv',
        'wizards/create_session_views.xml',
        'views/my_academy_course_views.xml',
        'views/my_academy_session_views.xml',
        'views/res_partner_views.xml',
        'views/my_academy_dashboards.xml',
        'views/my_academy_menus.xml',
        'report/session_report.xml',
        'report/session_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'data/my_academy_demo.xml',
    ],
}
