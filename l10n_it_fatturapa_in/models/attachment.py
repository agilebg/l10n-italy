#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

SELF_INVOICE_TYPES = (
    "TD16",
    "TD17",
    "TD18",
    "TD19",
    "TD20",
    "TD21",
    "TD22",
    "TD27",
    "TD28",
)


class FatturaPAAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment"
    _name = "fatturapa.attachment.in"
    _description = "Electronic Invoice"

    in_invoice_ids = fields.One2many(
        "account.move",
        "fatturapa_attachment_in_id",
        string="In Bills",
        readonly=True,
    )
    xml_supplier_id = fields.Many2one(
        "res.partner", string="Supplier", store=True
    )
    invoices_number = fields.Integer(
        "Bills Number", store=True
    )
    invoices_total = fields.Float(
        "Bills Total",
        store=True,
        help="If specified by supplier, total amount of the document net of "
        "any discount and including tax charged to the buyer/ordered",
    )
    invoices_date = fields.Char(
        string="Invoices date", store=True
    )
    registered = fields.Boolean(compute="_compute_registered", store=True)

    e_invoice_received_date = fields.Datetime(string="E-Bill Received Date")

    e_invoice_validation_error = fields.Boolean(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_validation_message = fields.Text(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_parsing_error = fields.Text(
        store=True,
    )

    is_self_invoice = fields.Boolean(
        "Contains self invoices", store=True
    )

    inconsistencies = fields.Text(store=True)

    linked_invoice_id_xml = fields.Char(
        store=True,
    )
    price_decimal_digits = fields.Integer(
        string="Prices decimal digits",
        help="Value used during import of this e-invoice "
        'to override "Product Price" precision.',
        readonly=True,
    )
    quantity_decimal_digits = fields.Integer(
        string="Quantities decimal digits",
        help="Value used during import of this e-invoice "
        'to override "Product Unit of Measure" precision.',
        readonly=True,
    )
    discount_decimal_digits = fields.Integer(
        string="Discounts decimal digits",
        help="Value used during import of this e-invoice "
        'to override "Discount" precision.',
        readonly=True,
    )

    _sql_constraints = [
        (
            "ftpa_attachment_in_name_uniq",
            "unique(att_name)",
            "The name of the e-bill file must be unique!",
        )
    ]

    @api.depends("in_invoice_ids.e_invoice_validation_error")
    def _compute_e_invoice_validation_error(self):
        for att in self:
            att.e_invoice_validation_error = False
            att.e_invoice_validation_message = False
            bills_with_error = att.in_invoice_ids.filtered(
                lambda b: b.e_invoice_validation_error
            )
            if not bills_with_error:
                continue
            att.e_invoice_validation_error = True
            errors_message_template = "{bill}:\n{errors}"
            error_messages = list()
            for bill in bills_with_error:
                error_messages.append(
                    errors_message_template.format(
                        bill=bill.display_name, errors=bill.e_invoice_validation_message
                    )
                )
            att.e_invoice_validation_message = "\n\n".join(error_messages)

    @api.depends("in_invoice_ids")
    def _compute_registered(self):
        for att in self:
            if att.in_invoice_ids and len(att.in_invoice_ids) == att.invoices_number:
                att.registered = True
            else:
                att.registered = False
