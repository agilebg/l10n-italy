# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    fatturapa_attachment_out_id = fields.Many2one(
        "fatturapa.attachment.out", "E-invoice Export File", readonly=True, copy=False
    )
    fatturapa_state = fields.Selection(
        [
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("accepted", "Accepted"),
            ("error", "Error"),
        ],
        string="E-invoice State",
        store="true",
    )
    fatturapa_payment_method_id = fields.Many2one(
        comodel_name="fatturapa.payment_method",
        string="Fiscal Payment Method",
        help="Fiscal Payment Method used in the e-invoice, "
        "defaults to the Payment Term's Fiscal Payment Method.",
        compute="_compute_fatturapa_payment_term_data",
        store=True,
        readonly=False,
    )
    fatturapa_payment_term_id = fields.Many2one(
        comodel_name="fatturapa.payment_term",
        string="Fiscal Payment Term",
        help="Fiscal Payment Term used in the e-invoice, "
        "defaults to the Payment Term's Fiscal Payment Term.",
        compute="_compute_fatturapa_payment_term_data",
        store=True,
        readonly=False,
    )

    @api.depends(
        "invoice_payment_term_id",
    )
    def _compute_fatturapa_payment_term_data(self):
        for invoice in self:
            payment_term = invoice.invoice_payment_term_id
            invoice.fatturapa_payment_method_id = (
                payment_term.fatturapa_pm_id or invoice.fatturapa_payment_method_id
            )
            invoice.fatturapa_payment_term_id = (
                payment_term.fatturapa_pt_id or invoice.fatturapa_payment_term_id
            )
