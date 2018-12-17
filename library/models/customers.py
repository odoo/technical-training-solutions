# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    author = fields.Boolean('is an Author', default=False)
    publisher = fields.Boolean('is a Publisher', default=False)

    current_rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals', domain=[('state', '=', 'rented')])
    old_rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals', domain=[('state', '=', 'returned')])
    lost_rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals', domain=[('state', '=', 'lost')])

    book_ids = fields.Many2many("product.product", string="Books", domain=[('book', '=', True)])
    copy_ids = fields.Many2many("library.copy", string="Book Copies")
    nationality_id = fields.Many2one('res.country', 'Nationality')
    birthdate = fields.Date('Birthdate')

    qty_lost_book = fields.Integer('Number of book copies lost', compute="_get_lost_books_qty")
    payment_ids = fields.One2many('library.payment', 'customer_id', string='Payments')
    amount_owed = fields.Float('Amount owed', compute="_amount_owed", store=True)

    @api.multi
    def _get_lost_books_qty(self):
        for rec in self:
            rec.qty_lost_book = len(rec.lost_rental_ids)

    @api.multi
    @api.depends('payment_ids.amount')
    def _amount_owed(self):
        for rec in self:
            rec.amount_owed = - sum(rec.payment_ids.mapped('amount'))


class Payment(models.Model):
    _name = 'library.payment'
    _description = 'Payment'

    date = fields.Date(required=True, default=fields.Date.context_today)
    amount = fields.Float()
    customer_id = fields.Many2one('res.partner', 'Customer', domain=[('customer', '=', True)])
