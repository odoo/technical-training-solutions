# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive",
        ), (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The offer price must be positive",
        ),
    ]

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("N", "North"),
            ("S", "South"),
            ("E", "East"),
            ("W", "West"),
        ],
        string="Garden Orientation",
    )

    # Special
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        compute="_compute_state",
        readonly=False,
        store=True,
    )
    active = fields.Boolean("Active", default=True)

    # Relational
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Computed
    date_availability = fields.Date(
        "Available From",
        compute='_compute_date_availability',
        store=True,
        readonly=False,
        copy=False,
    )
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )
    best_price = fields.Float(
        "Best Offer",
        compute="_compute_best_price",
        help="Best offer received",
    )

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0

    @api.depends('create_date')
    def _compute_date_availability(self):
        for prop in self:
            if not prop.date_availability:
                prop.date_availability = fields.Date.context_today(self) + relativedelta(months=3)

    @api.depends('offer_ids.state')
    def _compute_state(self):
        for prop in self:
            if 'accepted' in prop.offer_ids.mapped('state'):
                prop.state = 'offer_accepted'
            elif prop.offer_ids:
                prop.state = 'offer_received'
            else:
                prop.state = 'new'

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(
                    prop.selling_price,
                    prop.expected_price * 90.0 / 100.0,
                    precision_rounding=0.01
                ) < 0
            ):
                raise ValidationError(_(
                    "The selling price must be at least 90% of the expected price! "
                    "You must reduce the expected price if you want to accept this offer."
                ))

    @api.onchange("garden")
    def _onchange_garden(self):
        # Note this might be a bad usability feature.
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # ------------------------------------------ CRUD Methods -------------------------------------

    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError(_("Only new and canceled properties can be deleted."))
        return super().unlink()

    # ---------------------------------------- Action Methods -------------------------------------

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError(_("Canceled properties cannot be sold."))
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError(_("Sold properties cannot be canceled."))
        return self.write({"state": "canceled"})
