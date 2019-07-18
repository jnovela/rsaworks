from odoo import api, fields, models, _
from odoo.exceptions import UserError


class JobsStage(models.Model):
    _name = 'ssi_jobs_stage'
    _description = 'Jobs Stage'
    
    name = fields.Char(string='Name')
    display_name = fields.Char(string='Display Name', readonly=True, track_visibility="onchange")

    def _add_default_records_on_install(self):
        default_records = [
            'New Job',
            'Inspection',
            'Review',
            'Quotation Sent',
            'Awaiting Parts',
            'Under Repair',
            'Job Complete'
        ]
        for record in default_records:
            self.create({'name': record})