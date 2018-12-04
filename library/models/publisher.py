# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class Editor(models.Model):
    _name = 'library.publisher'
    _description = 'Library Publisher'

    name = fields.Char(string='Name')
