# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    price = fields.Float("Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)

    # Special
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("awaiting", "Awaiting")
        ],
        string="Status",
        copy=False,
        default="awaiting",
    )

    # Relational
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    # For stat button:
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    # Computed
    date = fields.Date(compute="_compute_date", readonly=False, store=True)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.date).days

    @api.depends('create_date')
    def _compute_date(self):
        for offer in self:
            offer.date = offer.date or fields.Date.context_today(offer)

    # ------------------------------------ Constraint Methods -------------------------------------

    @api.constrains('property_id')
    def _constrains_property_id(self):
        for offer in self:
            if offer.property_id.state in ('sold', 'canceled'):
                raise UserError(_("You can't make an offer for a Sold or Canceled property"))
            max_offer = max(offer.property_id.offer_ids, key=lambda o: o.price)
            if max_offer != offer:
                raise UserError(_("The offer must be higher than %.2f", max_offer.price))

    # ---------------------------------------- Action Methods -------------------------------------

    def action_accept(self):
        if "accepted" in self.property_id.offer_ids.mapped("state"):
            raise UserError(_("An offer as already been accepted."))
        self.state = 'accepted'
        self.property_id.write({
            "state": "offer_accepted",
            "selling_price": self.price,
            "buyer_id": self.partner_id.id,
        })

    def action_refuse(self):
        self.state = 'refused'
