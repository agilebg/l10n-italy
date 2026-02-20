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
