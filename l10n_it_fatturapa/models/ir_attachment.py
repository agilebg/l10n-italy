#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FatturaPAAttachment(models.Model):
    _name = "fatturapa.attachment"
    _description = "SdI file"
    _inherits = {
        "ir.attachment": "ir_attachment_id",
    }
    _inherit = [
        "mail.thread",
        "l10n_it_fatturapa.attachment.e_invoice.link",
    ]
    _order = "id desc"

    id = fields.Id()
    ir_attachment_id = fields.Many2one(
        comodel_name="ir.attachment",
        string="Attachment",
        required=True,
        ondelete="cascade",
    )
    att_name = fields.Char(
        string="SdI file name",
        related="ir_attachment_id.name",
        store=True,
    )
    ftpa_preview_link = fields.Char(
        "Preview link", readonly=True, compute="_compute_ftpa_preview_link"
    )

    def _compute_ftpa_preview_link(self):
        for att in self:
            att.ftpa_preview_link = (
                att.get_base_url() + "/fatturapa/preview/%s" % att.ir_attachment_id.id
            )
