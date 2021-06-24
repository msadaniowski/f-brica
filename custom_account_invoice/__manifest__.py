# -*- coding: utf-8 -*-
{
    'name': "custom_account_invoice",

    'summary': """
        Módulo""",

    'description': """
        Modulo...
    """,

    'author': "Odoo",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account' ,'purchase', 'product',  'sale', ],

    # always loaded
    'data': [

        # 'views/views_account_invoice.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
