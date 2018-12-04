# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Books(models.Model):
    _inherit = 'product.product'

    author_ids = fields.Many2many('res.partner', string="Authors", domain=[('author', '=', True)])
    edition_date = fields.Date(string='Edition date')
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one('res.partner', string='Publisher', domain=[('publisher', '=', True)])
    copy_ids = fields.One2many('library.copy', 'book_id', string="Book Copies")
    rental_ids = fields.One2many('library.rental', 'book_id', string='Rentals')
    book = fields.Boolean('is a book', default=False)
    book_state = fields.Selection([('available', 'Available'), ('rented', 'Rented'), ('lost', 'Lost')], default="available")


class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('product.product', string="Book", required=True, ondelete="cascade", delegate=True)
    reference = fields.Char(string="Reference")
    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
