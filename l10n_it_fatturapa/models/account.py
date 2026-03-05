# Copyright 2014 Davide Corio <davide.corio@abstract.it>

from odoo import api, fields, models


class FatturapaActivityProgress(models.Model):
    # _position = ['2.1.7']
    _name = "fatturapa.activity.progress"
    _description = "E-invoice activity progress"

    fatturapa_activity_progress = fields.Integer("Activity Progress")
    invoice_id = fields.Many2one(
        "account.move", "Related Invoice", ondelete="cascade", index=True
    )

class FatturapaSummaryData(models.Model):
    # _position = ['2.2.2']
    _name = "fatturapa.summary.data"
    _description = "E-invoice summary data"
    tax_rate = fields.Float("Tax Rate")

    @api.model
    def _get_tax_kinds(self):
        return [(t.code, t.name) for t in self.env["account.tax.kind"].search([])]

    non_taxable_nature = fields.Selection(
        selection="_get_tax_kinds",
        string="Non taxable nature",
    )
    incidental_charges = fields.Float("Incidental Charges")
    rounding = fields.Float("Rounding")
    amount_untaxed = fields.Float("Amount Untaxed")
    amount_tax = fields.Float("Amount Tax")
    payability = fields.Selection(
        [
            ("I", "Immediate payability"),
            ("D", "Deferred payability"),
            ("S", "Split payment"),
        ],
        string="VAT payability",
    )
    law_reference = fields.Char("Law reference", size=128)
    invoice_id = fields.Many2one(
        "account.move", "Related Invoice", ondelete="cascade", index=True
    )


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

class AccountInvoice(models.Model):
    # _position = ['2.1', '2.2', '2.3', '2.4', '2.5']
    _inherit = "account.move"

    carrier_id = fields.Many2one("res.partner", string="Carrier", copy=False)
    transport_vehicle = fields.Char("Vehicle", size=80, copy=False)
    transport_reason = fields.Char("Reason", size=80, copy=False)
    number_items = fields.Integer("Number of Items", copy=False)
    description = fields.Char(size=100, copy=False)
    unit_weight = fields.Char("Weight Unit", size=10, copy=False)
    gross_weight = fields.Float(copy=False)
    net_weight = fields.Float(copy=False)
    pickup_datetime = fields.Datetime("Pick up", copy=False)
    transport_date = fields.Date(copy=False)
    delivery_address = fields.Text("Delivery Address for E-invoice", copy=False)
    delivery_datetime = fields.Datetime("Delivery Date Time", copy=False)
    ftpa_incoterms = fields.Char(string="E-inv Incoterms", copy=False)
    vehicle_registration = fields.Date(copy=False)
    total_travel = fields.Char("Travel in hours or Km", size=15, copy=False)

class AccountInvoiceLine(models.Model):
    # _position = ['2.2.1']
    _inherit = "account.move.line"

    ftpa_line_number = fields.Integer("Line Number", readonly=True, copy=False)
