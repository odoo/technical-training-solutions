# -*- coding: utf-8 -*-
from odoo import models, fields


class Partner(models.Model):
    _name = 'coopplanning.partner'
    _description = 'Partner'

    name = fields.Char(required=True)
