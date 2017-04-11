# -*- coding: utf-8 -*-
{
    'name': "prasetia-hr",

    'summary': """
        Module Human Resource In Prasetia""",

    'description': """
        No Description For Now
    """,

    'author': "Junifar Hidayat",
    'website': "http://www.junifar.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'prasetia',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/hr.xml',
        'views/family.xml',
        'views/education.xml',
        'views/device.xml',
        'views/attendance_import.xml',
        'views/attendance.xml',
        'views/attendance_report.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}