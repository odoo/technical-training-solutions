# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'

    customer_id = fields.Many2one('library.partner', string='Customer')
    copy_id = fields.Many2one('library.copy', string="Book Copy")
    book_id = fields.Many2one('library.book', string='Book', related='copy_id.book_id', readonly=True)
    rental_date =  fields.Date(string='Rental date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return date')
    book_title = fields.Char(related='book_id.name', string='Title')
    book_author = fields.Many2many('library.partner', related='book_id.author_ids', string='Authors')
    book_publisher = fields.Many2one('library.publisher', related='book_id.publisher_id', string='Publisher')