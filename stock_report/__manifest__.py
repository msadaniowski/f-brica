# -*- coding: utf-8 -*-
{
    'name': "stock_report",

    'summary': """
        """,

    'description': """
          """,

    'author': "Sadaniowski Mauricio",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['product', 'stock',],

    # always loaded
    'data': [
        'views/stock_report.xml',
        'views/stock_report_views.xml',
        'views/product_template_inherited.xml',
    ],
}


