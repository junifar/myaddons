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
        'views/attendance_import_workflow.xml',
        'views/attendance.xml',
        'views/attendance_report.xml',
        'views/leave_request.xml',
        'views/leave_request_workflow.xml',
        'views/print_leave_form.xml',
        'views/leave_request_type.xml',
        'views/menus.xml',
        'wizard/personal_absen_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
