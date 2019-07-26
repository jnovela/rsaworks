# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class Partner(models.Model):

    _inherit = 'res.partner'

    project_manager_id = fields.Many2one('res.users', string='Project Manager', track_visibility='onchange', default=lambda self: self.env.user)
