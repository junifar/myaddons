# -*- coding: utf-8 -*-
{
    'name': "Prasetia Project",

    'summary': """
        Prasetia Project""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Junifar Hidayat",
    'website': "http://www.prasetia.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'prasetia',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/areas.xml',
        'views/islands.xml',
        'views/provinces.xml',
        'views/cities.xml',
        'views/field_types.xml',
        'views/sites.xml',
        'views/menus.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'auto_install': False,
}