# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class Jobs(models.Model):
    _name = 'ssi_jobs'
    _description = 'Jobs'
    _order = "create_date,display_name desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # TOP
    order_total = fields.Monetary(
        string='Order Total', track_visibility='always', related='so_ids.amount_total')
    so_ids = fields.One2many(
        'sale.order', 'ssi_job_id', string='SO')

    # REFERS TO FIELD INSIDE SAME MODEL
    # x_studio_sale_order.amount_total

    # LEFT
    name = fields.Char(required=True, index=True)
    customer_id = fields.Many2one(
        'res.partner', string='Customer', domain="[('customer', '=', 1)]")
    objects = fields.Selection(
        [('motor', 'Motor'), ('generator', 'Generator'), ('coil', 'Coil'), ('brake', 'Brake'), ('other', 'Other')], string='Object')
    size = fields.Integer(string='Size')
    sizeUM = fields.Selection(
        [('hp', 'Horsepower'), ('kw', 'Kilowatts'), ('lb-ft', 'Torque')], string='Size UM')
    shaft = fields.Selection(
        [('horizontal', 'Horizontal'), ('vertical', 'Vertical'), ('other', 'Other')], string='Shaft')
    dimensions = fields.Float(string='Dimensions')

    # RIGHT
    ready_for_pickup = fields.Datetime(string='Ready for Pickup')
    urgency = fields.Selection(
        [('straight', 'Straight time'), ('straight_quote', 'Straight time quote before repair'), ('overtime', 'Overtime'), ('overtime_quote', 'Overtime quote before repair')], string='Urgency')
    po_number = fields.Char(string='PO Number')
    weight = fields.Float(string='Weight')
    weightUM = fields.Selection(
        [('lbs', 'pounds'), ('tons', 'tons'), ('kgs', 'kilograms')], string='Weight UM')
    notes = fields.Text(string='Notes')
    status = fields.Selection(
        [('ready', 'Ready'), ('process', 'In Process'), ('done', 'Complete'), ('blocked', 'Blocked')], string='Status')

    # OTHER
    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='restrict', required=True,
        domain=[('parent_id', '=', False)])
    active = fields.Boolean(default=True)

    _sql_constraints = [(
        'name_unique',
        'unique(name)',
        'This job name already exists in the system!'
    )]
