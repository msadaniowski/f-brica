# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInherit(models.Model):
    _inherit = 'account.invoice.report'

    main_sellers_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        readonly=True,
        store=True,
        related="main_seller_ids.product_id.main_seller_id",)
