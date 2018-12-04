# -*- coding: utf-8 -*-
import math
from datetime import datetime
from pytz import UTC

from odoo import models, fields, api


def float_to_time(f):
    decimal, integer = math.modf(f)
    return "%s:%s" % (str(int(integer)).zfill(2), str(int(round(decimal * 60))).zfill(2))

def floatime_to_hour_minute(f):
    decimal, integer = math.modf(f)
    return int(integer), int(round(decimal * 60))


class TaskType(models.Model):
    _name = 'coopplanning.task.type'
    _description = "Task Type"

    name = fields.Char()
    description = fields.Text()
    area = fields.Char()
    active = fields.Boolean(default=True)


class DayNumber(models.Model):
    _name = 'coopplanning.daynumber'
    _description = "Day Of Week Number"

    name = fields.Char()
    number = fields.Integer("Day Number",
                            help="From 1 to N, When you will instanciate your planning, Day 1 will be the start date of the instance, Day 2 the second, etc...")
    active = fields.Boolean(default=True)


class TaskTemplate(models.Model):
    _name = 'coopplanning.task.template'
    _description = "Task Template"

    name = fields.Char(required=True)
    day_nb_id = fields.Many2one('coopplanning.daynumber', string='Day')
    task_type_id = fields.Many2one('coopplanning.task.type', string="Task Type")
    start_time = fields.Float()
    end_time = fields.Float()

    duration = fields.Float(string="Duration", compute='_get_duration', help="Duration in Hour", store=True)
    worker_nb = fields.Integer(string="Number of worker", help="Max number of worker for this task", default=1)
    worker_ids = fields.Many2many('res.partner', string="Recurrent worker assigned")
    active = fields.Boolean(default=True)
    day_nb = fields.Integer(related='day_nb_id.number', string='Day Number')
    task_area = fields.Char(related='task_type_id.area', string='Task Area')
    floating = fields.Boolean("Floating Task", help="This task will be not assigned to someone and will be available for non recurring workers")

    @api.depends('start_time', 'end_time')
    def _get_duration(self):
        for rec in self:
            rec.duration = rec.end_time - rec.start_time


class Partner(models.Model):
    _name = 'coopplanning.partner'
    _description = "Partner"

    #Solution : Empty the field worker_ids when floating is selected to be sure no worker will be pre assigned to the task
    @api.onchange('floating')
    def _onchange_floating(self):
        if self.floating:
            self.worker_ids = self.env['res.partner']
