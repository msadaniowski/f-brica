# -*- coding: utf-8 -*-
{
    'name': "Stock Real",

    'summary': """
        """,

    'description': """
        Muestra el stock actual sin considerar las que van a ingresar debido a una orden de fabricacion o una compra
    """,

    'author': "Sadaniowski Mauricio",
   

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
     
       'views/views.xml',
       
      
    ],
    # only loaded in demonstration mode
    'demo': [
    #    'demo/demo.xml',
    ],
}
