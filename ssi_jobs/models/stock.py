# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    so_job_id = fields.Many2one('ssi_jobs', related='sale_id.ssi_job_id', string='SO Job')
    po_job_id = fields.Many2one('ssi_jobs', related='purchase_id.ssi_job_id', string='PO Job')

