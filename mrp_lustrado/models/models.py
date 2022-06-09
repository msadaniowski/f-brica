# Copyright YEAR(S), AUTHOR(S)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class mrpProductiones(models.Model):
    _inherit = 'mrp.production'

    lustre = fields.Char(string='Lustre', compute='compute_variant', store='true')
    tapizado = fields.Char(string='Tapizado', compute='compute_variant', store='true')

    @api.depends('product_id')
    def compute_variant(self):
        for record in self:
            _logger.info('Record %s' % record.name)

            lustre = record.product_id.product_template_attribute_value_ids.filtered(
                lambda x: x.attribute_id.name == 'Lustre')
            _logger.info('lustre %s' % lustre)

            if lustre:
                record.lustre = lustre.name
            else:
                record.lustre = False
            tapizado = record.product_id.product_template_attribute_value_ids.filtered(
                lambda x: x.attribute_id.name == 'Tapizado')
            _logger.info('tapizado %s' % tapizado)

            if tapizado:
                record.tapizado = tapizado.name
            else:
                record.tapizado = False


class InventarySalesTravel(models.Model):  # FUNCION DEL NRO DE VIAJE
    _inherit = 'stock.picking'
    client_order_nro = fields.Char('Viaje', related="group_id.sale_id.client_order_ref", store='true')

  

