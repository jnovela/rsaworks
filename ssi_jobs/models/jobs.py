# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class Jobs(models.Model):
    _name = 'ssi.jobs'
    _description = 'Jobs'
    _order = "create_date,display_name desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, index=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='restrict', required=True,
        domain=[('parent_id', '=', False)])
    active = fields.Boolean(default=True)

    _sql_constraints = [(
        'name_unique',
        'unique(name)',
        'This job name already exists in the system!'
        )]
