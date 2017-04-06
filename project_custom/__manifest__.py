# -*- coding: utf-8 -*-
{
    'name': "Project Improvement",

    'summary': """
        Customization existing official module project ODOO
        improve dashboard interface
        """,

    'description': """
        Project Improvement
    """,

    'author': "RubahApi",
    'website': "http://www.junifar.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/project_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'auto_install': False,
}