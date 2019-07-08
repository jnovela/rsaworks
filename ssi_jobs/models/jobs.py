# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class Jobs(models.Model):
    _name = 'ssi_jobs'
    _description = 'Jobs'
    _order = "create_date,display_name desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # TOP
    so_ids = fields.One2many(
        'sale.order', 'ssi_job_id', string='SO')
    order_total = fields.Monetary(
        string='Order Total', track_visibility='always', related='so_ids.amount_total')
    po_count = fields.Integer(string='Purchase Order', compute='_get_po_count')

    currency_id = fields.Many2one('res.currency', string='Account Currency',
                                  help="Forces all moves for this account to have this account currency.")

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

    @api.depends('order_total')
    def _get_po_count(self):
        results = self.env['purchase.order'].read_group(
            [('ssi_job_id', 'in', self.ids)], 'ssi_job_id', 'ssi_job_id')
        dic = {}
        for x in results:
            dic[x['ssi_job_id'][0]] = x['x_studio_job_count']
        for record in self:
            record['po_count'] = dic.get(
                record.id, 0)
