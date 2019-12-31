# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    project_manager = fields.Many2one('res.users', string='Project Manager')

