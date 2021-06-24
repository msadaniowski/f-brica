# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInherit(models.Model):
    _inherit = 'account.invoice.report'

    # main_seller_id = fields.Many2one(related='test.product_id.main_seller_id', readonly=True, string='Proveedor')
    main_seller_ids = fields.Many2one('res.partner')
    nro_viaje = fields.Char(related='main_seller_ids.product_id.main_seller_id', string='Proveedor')