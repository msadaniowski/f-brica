# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInherit(models.Model):
    _inherit = 'account.invoice.report'

    name = fields.Char(string='Descripción')

    test = fields.Many2one(comodel_name='res.partner')
    main_seller_id = fields.Many2one(related='test.product_id.main_seller_id',
                                     readonly=True,
                                     store=True,
                                     string='Proveedor')
