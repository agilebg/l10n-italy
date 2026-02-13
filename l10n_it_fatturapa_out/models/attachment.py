# Copyright 2014 Davide Corio
# Copyright 2016-2018 Lorenzo Battistini - Agile Business Group
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class FatturaPAAttachment(models.Model):
    _name = "fatturapa.attachment.out"
    _description = "Electronic Invoice"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = [
        "fatturapa.attachment",
        "l10n_it_fatturapa.attachment.e_invoice.link",
    ]
    _order = "id desc"

    has_pdf_invoice_print = fields.Boolean(
        help="True if all the invoices have a printed "
        "report attached in the XML, False otherwise.",
        compute="_compute_has_pdf_invoice_print",
        store=True,
    )
    invoice_partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        store=True,
        compute="_compute_invoice_partner_id",
    )
    state = fields.Selection(
        selection=[
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("sender_error", "Sender Error"),
            ("recipient_error", "Not delivered"),
            ("rejected", "Rejected (PA)"),
            ("validated", "Delivered"),
            ("accepted", "Accepted"),
        ],
        string="State",
        default="ready",
        tracking=True,
    )
    sending_user = fields.Many2one(
        comodel_name="res.users",
        string="Sending User",
        readonly=True,
    )
    sending_date = fields.Datetime("Sent Date", readonly=True)
    delivered_date = fields.Datetime("Delivered Date", readonly=True)

    def _compute_invoice_partner_id(self):
        for att in self:
            partners = att.mapped("out_invoice_ids.partner_id")
            att.invoice_partner_id = False
            if len(partners) == 1:
                att.invoice_partner_id = partners.id

    def _compute_has_pdf_invoice_print(self):
        """Check if all the invoices related to this attachment
        have at least one attachment containing
        the PDF report of the invoice"""
        for attachment_out in self:
            attachment_out.has_pdf_invoice_print = False
            for invoice in attachment_out.out_invoice_ids:
                invoice_attachments = invoice.fatturapa_doc_attachments
                if not any([ia.is_pdf_invoice_print for ia in invoice_attachments]):
                    break
            else:
                # We have examined all the invoices and none of them
                # has caused a break, this means all the invoices have at least
                # one attachment having is_pdf_invoice_print = True
                attachment_out.has_pdf_invoice_print = True
