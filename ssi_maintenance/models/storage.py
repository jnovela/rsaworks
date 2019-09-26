# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Storage(models.Model):
    _name = "storage"
    _description = "Equipment Storage Records"

    location_id = fields.Char(string='Location')
    equipment_id = fields.Many2one(
        'maintenance.equipment', string='Equipment', ondelete='cascade')
    subscription_id = fields.Many2one('sale.subscription', string='Subscription')
    check_in = fields.Datetime(string='Check in')
    check_out = fields.Datetime(string='Check out')
    equip_square_feet = fields.Float(string='Square Feet', related='equipment_id.square_feet')
    equip_serial_no = fields.Char(string='Serial Number', related='equipment_id.serial_no')
    status = fields.Boolean(string='Status')
