# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class WC(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    ssi_job_id = fields.Many2one(
        'ssi_jobs', string='Job')