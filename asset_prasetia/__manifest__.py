{
    'name': "prasetia Asset COntoh",

    'summary': """
        Asset For Prasetia""",

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
        'views/barang_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
