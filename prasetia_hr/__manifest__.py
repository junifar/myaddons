{
    'name': "prasetia human resource",

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
    'depends': ['base', 'hr', 'report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/prasetia_hr_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/hr.xml',
        'views/family.xml',
        'views/education.xml',
        'views/device.xml',
        'views/contract.xml',
        'views/organization_structure.xml',
        'views/directorate.xml',
        'views/absen_book.xml',
        'views/calendar_tahunan.xml',
        'views/kartu_keluarga.xml',
        'views/attendance_import.xml',
        'views/attendance_import_workflow.xml',
        'views/attendance.xml',
        'views/attendance_report.xml',
        'views/print_leave_form.xml',
        'views/leave_request.xml',
        'views/employee_office_area.xml',
        'data/leave_category_data.xml',
        'views/leave_request_workflow.xml',
        'views/leave_request_type.xml',
        'views/show_bank_information.xml',
        'views/leave_administration.xml',
        'views/menus.xml',
        'views/report_personal_leave.xml',
        'views/report_personal_absen.xml',
        'views/report_absen.xml',
        'views/report_family.xml',
        'views/report_organization_structure.xml',
        'views/prasetia_hr_report.xml',
        'wizard/personal_absen_views.xml',
        'wizard/personal_leave_views.xml',
        'wizard/report_absen_wizard_views.xml',
        'wizard/external_data_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
