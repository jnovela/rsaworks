# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class SO(models.Model):
    _inherit = 'sale.order'

    ssi_job_id = fields.Many2one('ssi_jobs', string='Job')
    
    @api.onchange('ssi_job_id')
    def _onchange_ssi_job_id(self):
        # When updating jobs dropdown, auto set analytic account.
        if self.ssi_job_id.aa_id:
            self.analytic_account_id = self.ssi_job_id.aa_id
    
class PO(models.Model):
    _inherit = 'purchase.order'

    ssi_job_id = fields.Many2one('ssi_jobs', string='Job')

    @api.onchange('ssi_job_id')
    def _onchange_ssi_job_id(self):
        # When updating jobs dropdown, auto set analytic account on po lines.
        if self.ssi_job_id.aa_id:
            for line in self.order_line:
                line.account_analytic_id = self.ssi_job_id.aa_id
    