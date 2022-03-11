# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models, api

class ProductLabel(models.Model):
    _inherit = 'product.template'
    
    etiquetas = fields.Char(string='Etiquetas', store='true')

