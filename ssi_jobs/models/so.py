# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class MaintenanceEquipment(models.Model):
    _inherit = 'sale.order'

    ssi_job_id = fields.One2many(
        'ssi_jobs', string='Job')
