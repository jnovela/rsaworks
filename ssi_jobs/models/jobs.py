# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Jobs(models.Model):
    _name = 'ssi_jobs'
    _description = 'Jobs'
    _order = "create_date,display_name desc"
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    # TOP AND RELATED
    so_ids = fields.One2many(
        'sale.order', 'ssi_job_id', string='SO')
    order_total = fields.Monetary(
        string='Order Total', track_visibility='always', related='so_ids.amount_total')
    # po_count = fields.Integer(string='Purchase Order', compute='_get_po_count')
    # ai_count = fields.Integer(string='Vendor Bills', compute='_get_ai_count')
    # prod_count = fields.Integer(string='Operations', compute='_get_prod_count')
    # wo_count = fields.Integer(string='Work Orders', compute='_get_wo_count')
    # wc_count = fields.Integer(string='Job Count', compute='_get_wc_count')

    # NECESSARY SUPPORT
    currency_id = fields.Many2one('res.currency', string='Account Currency',
                                  help="Forces all moves for this account to have this account currency.")

    # LEFT
    name = fields.Char(required=True, index=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='restrict', required=True,
        domain=[('parent_id', '=', False)])
    active = fields.Boolean(default=True)
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

    _sql_constraints = [(
        'name_unique',
        'unique(name)',
        'This job name already exists in the system!'
    )]

    # ACTION TO LEAD TO TABLE WITH SOs
    @api.one
    def action_view_estimates(self):
        self.ensure_one()
        action = self.env.ref(
            'ssi_jobs.sale_order_estimate_line_action').read()[0]
        # raise UserError(_(action))

        # action['domain'] = [('ssi_job_id', '=', self.id)]
        return action

    # <record id="stock_move_line_action" model="ir.actions.act_window">
    #         <field name="name">Product Moves</field>
    #         <field name="res_model">stock.move.line</field>
    #         <field name="type">ir.actions.act_window</field>
    #         <field name="view_type">form</field>
    #         <field name="view_mode">tree,kanban,pivot,form</field>
    #         <field name="view_id" ref="view_move_line_tree"/>
    #         <field name="context">{'search_default_done': 1, 'search_default_groupby_product_id': 1}</field>
    #         <field name="help" type="html">
    #           <p class="o_view_nocontent_empty_folder">
    #             There's no product move yet
    #           </p>
    #         </field>
    # </record>

    # @api.depends('order_total')
    # def _get_po_count(self):
    #     results = self.env['purchase.order'].read_group(
    #         [('ssi_job_id', 'in', self.ids)], 'ssi_job_id', 'ssi_job_id')
    #     dic = {}
    #     for x in results:
    #         dic[x['ssi_job_id'][0]] = x['ssi_job_id_count']
    #     for record in self:
    #         record.po_count = dic.get(
    #             record.id, 0)

    # @api.depends('order_total')
    # def _get_ai_count(self):
    #     results = self.env['account.invoice'].read_group(
    #         [('ssi_job_id', 'in', self.ids)], 'ssi_job_id', 'ssi_job_id')
    #     dic = {}
    #     for x in results:
    #         dic[x['ssi_job_id'][0]] = x['ssi_job_id_count']
    #     for record in self:
    #         record.ai_count = dic.get(
    #             record.id, 0)

    # @api.depends('order_total')
    # def _get_prod_count(self):
    #     results = self.env['mrp.production'].read_group(
    #         [('ssi_job_id', 'in', self.ids)], 'ssi_job_id', 'ssi_job_id')
    #     dic = {}
    #     for x in results:
    #         dic[x['ssi_job_id'][0]] = x['ssi_job_id_count']
    #     for record in self:
    #         record.ai_count = dic.get(
    #             record.id, 0)

    # @api.depends('order_total')
    # def _get_wo_count(self):
    #     results = self.env['mrp.workorder'].read_group(
    #         [('ssi_job_id', 'in', self.ids)], 'ssi_job_id', 'ssi_job_id')
    #     dic = {}
    #     for x in results:
    #         dic[x['ssi_job_id'][0]] = x['ssi_job_id_count']
    #     for record in self:
    #         record.ai_count = dic.get(
    #             record.id, 0)

    # @api.depends('order_total')
    # def _get_wc_count(self):
    #     results = self.env['mrp.workcenter.productivity'].read_group(
    #         [('ssi_job_id', 'in', self.ids)], 'ssi_job_id', 'ssi_job_id')
    #     dic = {}
    #     for x in results:
    #         dic[x['ssi_job_id'][0]] = x['ssi_job_id_count']
    #     for record in self:
    #         record.ai_count = dic.get(
    #             record.id, 0)
