# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class EstateReport(models.Model):
    _name = 'estate.report'
    _description = "Stock Report"
    _rec_name = 'id'
    _auto = False

    id = fields.Integer("", readonly=True)
    offer_state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Offer Status",
        readonly=True)
    property_id = fields.Many2one("estate.property", string="Property", readonly=True)
    property_state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Property Status",
        readonly=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", readonly=True)

    def _select(self):
        select_str = """
            po.id AS id,
            po.state AS offer_state,
            p.id AS property_id,
            p.state AS property_state,
            pt.id AS property_type_id
        """

        return select_str

    def _from(self):
        from_str = """
            estate_property_offer po
            LEFT JOIN estate_property p ON po.property_id = p.id
            LEFT JOIN estate_property_type pt ON po.property_type_id = pt.id
        """

        return from_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
                               SELECT
                                %s
                               FROM
                                %s
            )""" % (self._table, self._select(), self._from()))
