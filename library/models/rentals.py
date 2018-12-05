# -*- coding: utf-8 -*-
from odoo import models, fields


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('library.partner', string='Customer')
    book_id = fields.Many2one('library.book', string='Book')
    rental_date = fields.Date(string='Rental date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return date')

    book_name = fields.Char(related='book_id.name', string='Title')
    book_authors = fields.Many2many(related='book_id.authors_ids', string='Authors')
    book_edition_date = fields.Date(related='book_id.edition_date', string='Edition date')
