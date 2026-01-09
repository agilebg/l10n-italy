# Copyright 2014 Davide Corio <davide.corio@abstract.it>

from odoo import fields, models


class FatturaAttachments(models.Model):
    # _position = ['2.5']
    _name = "fatturapa.attachments"
    _description = "E-invoice attachments"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = ["l10n_it_fatturapa.attachment.e_invoice.link"]

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    compression = fields.Char(size=10)
    format = fields.Char(size=10)
    invoice_id = fields.Many2one(
        "account.move", "Related Invoice", ondelete="cascade", index=True
    )

