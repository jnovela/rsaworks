# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class WO(models.Model):
    _inherit = 'mrp.workorder'

    ssi_job_id = fields.Many2one(
        'ssi_jobs', string='Job')
