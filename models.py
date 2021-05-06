
# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class mrpProduction(models.Model):
    _name = 'mrp.production'

    color_id = fields.Many2one(
        'product.attribute.value',
        string='Color',
        compute='compute_variant',
        store = True,
    )
    material_id = fields.Many2one(
        'product.attribute.value',
        string='material',
        compute='compute_variant',
        store = True,
    )       

    def compute_variant(self):
        for record in self:
            color = record.product_id.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.name =='color')
            if color:
                record.color_id = color.id
               else:
                record.color_id = False
            material = record.product_id.product_template_attribute_value_ids.filtered(lambda x: x.attribute_id.name =='material')
            if material:
                record.material_id =material.id
            else:
                record.material_id = False
