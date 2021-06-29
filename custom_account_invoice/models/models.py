# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInherit(models.Model):
    _inherit = 'account.invoice.report'

    main_sellers_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        readonly=True,
        store=True,
        related="product_id.main_seller_id",)

    def _select(self):
        return super(AccountInvoiceReport, self)._select() + ", supp.name as main_sellers_id"

    def _from(self):
        return super(AccountInvoiceReport, self)._from() + " LEFT JOIN product_main_seller_id supp ON pt.id = supp.product_tmpl_id "

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ",supp.name "