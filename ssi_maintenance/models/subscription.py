# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
import requests


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'
    
#     equip_id = fields.Char(string='Equip_id')
    storage_id = fields.One2many('storage', 'subscription_id', string='Storage')
    square_foot_total = fields.Float(string='Square Foot Total', compute='_get_sqf_total')

    # ACTIONS AND METHODS
    @api.depends('storage_id')
    def _get_sqf_total(self):
        total = 0
        for record in self:
            for strg in record.storage_id:
                total = total + strg.equip_square_feet
            record.square_foot_total = total

