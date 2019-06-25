# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    rating_unit = fields.Selection([('HP', 'HP'), ('KW', 'KW'), ('FT-lbs', 'FT-lbs'), ('MW', 'MW')], string='Rating Unit')
