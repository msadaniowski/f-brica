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
    'depends': ['base', 'account','purchase','product','l10n_ar','l10n_latam_invoice_document','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_account_invoice.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
