# -*- coding: utf-8 -*-

from odoo import models, fields

class CustomProduct(models.Model):
    _inherit = 'product.product'

    quantity_difference = fields.Float(compute='_compute_quantity_difference')

    def _compute_quantity_difference(self):
        for product in self:
            product.quantity_difference = product.qty_available - product.outgoing_qty

class CustomProducts1(models.Model):
    _inherit = 'product.product'

    performance = fields.Float(string='Rendimiento')
    total_performance = fields.Float(compute='_compute_total_performance', string='Proyección estimada')

    def _compute_total_performance(self):
        for product in self:
            product.total_performance = product.qty_available * product.performance
