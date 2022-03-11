# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class mrpProductiones(models.Model):
    _inherit = 'product.template'

    
    Talle = fields.Char(string='Talle', compute='compute_variant', store='true')

    @api.depends('product_id')
    def compute_variant(self):
        for record in self:
            _logger.info('Record %s' % record.name)

            lustre = record.product_id.product_template_attribute_value_ids.filtered(
                lambda x: x.attribute_id.name == 'Talle')
            _logger.info('Talle %s' % Talle)

            if Talle:
                record.Talle = Talle.name
            else:
                record.Talle = False
           
