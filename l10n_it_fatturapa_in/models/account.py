#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    fatturapa_attachment_in_id = fields.Many2one(
        "fatturapa.attachment.in", "E-bill Import File", ondelete="restrict", copy=False
    )
    e_invoice_reference = fields.Char(
        string="E-invoice vendor reference", readonly=True
    )

class FatturapaArticleCode(models.Model):
    # _position = ['2.2.1.3']
    _name = "fatturapa.article.code"
    _description = "E-bill Article Code"

    name = fields.Char("Code Type")
    code_val = fields.Char("Code Value")
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )

class DiscountRisePrice(models.Model):
    _inherit = "discount.rise.price"
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )

class EInvoiceLine(models.Model):
    _name = "einvoice.line"
    _description = "E-invoice line"
    invoice_id = fields.Many2one(
        "account.move", "Bill", readonly=True, ondelete="cascade"
    )
    line_number = fields.Integer("Line Number", readonly=True)
    service_type = fields.Char("Sale Provision Type", readonly=True)
    cod_article_ids = fields.One2many(
        "fatturapa.article.code", "e_invoice_line_id", "Articles Code", readonly=True
    )
    name = fields.Char("Description", readonly=True)
    qty = fields.Float("Quantity", readonly=True, digits="Product Unit of Measure")
    uom = fields.Char("Unit of measure", readonly=True)
    period_start_date = fields.Date("Period Start Date", readonly=True)
    period_end_date = fields.Date("Period End Date", readonly=True)
    unit_price = fields.Float("Unit Price", readonly=True, digits="Product Price")
    discount_rise_price_ids = fields.One2many(
        "discount.rise.price",
        "e_invoice_line_id",
        "Discount and Supplement Details",
        readonly=True,
    )
    total_price = fields.Float("Total Price", readonly=True)
    tax_amount = fields.Float("VAT Rate", readonly=True)
    wt_amount = fields.Char("Tax Withholding", readonly=True)
    tax_kind = fields.Char("Nature", readonly=True)
    admin_ref = fields.Char("Administration Reference", readonly=True)
    other_data_ids = fields.One2many(
        "einvoice.line.other.data",
        "e_invoice_line_id",
        string="Other Administrative Data",
        readonly=True,
    )

class EInvoiceLineOtherData(models.Model):
    _name = "einvoice.line.other.data"
    _description = "E-invoice line other data"

    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )
    name = fields.Char("Data Type", readonly=True)
    text_ref = fields.Char("Text Reference", readonly=True)
    num_ref = fields.Float("Number Reference", readonly=True)
    date_ref = fields.Char("Date Reference", readonly=True)
