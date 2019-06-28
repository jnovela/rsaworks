# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Storage(models.Model):
    _name = "storage"

    location_id = fields.Char(string='Location')
    equipment_id = fields.Many2one('maintenance.equipment', 'Equipment')
    check_in = fields.Datetime(string='Check in')
    check_out = fields.Datetime(string='Check out')
    status = fields.Boolean(string='Status')