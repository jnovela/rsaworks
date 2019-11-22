# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import api, fields, models, tools, _
from odoo.osv import expression
from odoo.exceptions import UserError


class SO(models.Model):
    _inherit = 'sale.order'

    ssi_job_id = fields.Many2one('ssi_jobs', string='Job')
    job_stage = fields.Char(compute='_get_job_stage', string='Job Stage', readonly=True)
    
    @api.onchange('ssi_job_id')
    def _onchange_ssi_job_id(self):
        # When updating jobs dropdown, auto set analytic account.
        if self.ssi_job_id.aa_id:
            self.analytic_account_id = self.ssi_job_id.aa_id

    @api.depends('ssi_job_id')
    def _get_job_stage(self):
        for record in self:
            record.job_stage = record.ssi_job_id.stage_id.name
#         record.job_stage = record.ssi_job_id.stage_id.name

    @api.depends('state', 'order_line.invoice_status', 'order_line.invoice_lines')
    def _get_invoiced(self):
        """
        Compute the invoice status of a SO. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          invoice. This is also the default value if the conditions of no other status is met.
        - to invoice: if any SO line is 'to invoice', the whole SO is 'to invoice'
        - invoiced: if all SO lines are invoiced, the SO is invoiced.
        - upselling: if all SO lines are invoiced or upselling, the status is upselling.

        The invoice_ids are obtained thanks to the invoice lines of the SO lines, and we also search
        for possible refunds created directly from existing invoices. This is necessary since such a
        refund is not directly linked to the SO.
        """
        # Ignore the status of the deposit product
        deposit_product_id = self.env['sale.advance.payment.inv']._default_product_id()
        line_invoice_status_all = [(d['order_id'][0], d['invoice_status']) for d in self.env['sale.order.line'].read_group([('order_id', 'in', self.ids), ('product_id', '!=', deposit_product_id.id)], ['order_id', 'invoice_status'], ['order_id', 'invoice_status'], lazy=False)]
        for order in self:
            invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id').filtered(lambda r: r.type in ['out_invoice', 'out_refund'])
            # Search for invoices which have been 'cancelled' (filter_refund = 'modify' in
            # 'account.invoice.refund')
            # use like as origin may contains multiple references (e.g. 'SO01, SO02')
            refunds = invoice_ids.search([('origin', 'like', order.name), ('company_id', '=', order.company_id.id), ('type', 'in', ('out_invoice', 'out_refund'))])
            invoice_ids |= refunds.filtered(lambda r: order.name in [origin.strip() for origin in r.origin.split(',')])

            # Search for refunds as well
            domain_inv = expression.OR([
                ['&', ('origin', '=', inv.number), ('journal_id', '=', inv.journal_id.id)]
                for inv in invoice_ids if inv.number
            ])
            if domain_inv:
                refund_ids = self.env['account.invoice'].search(expression.AND([
                    ['&', ('type', '=', 'out_refund'), ('origin', '!=', False)], 
                    domain_inv
                ]))
            else:
                refund_ids = self.env['account.invoice'].browse()

            line_invoice_status = [d[1] for d in line_invoice_status_all if d[0] == order.id]

            if order.ssi_job_id:
                if order.state not in ('sale', 'done'):
                    invoice_status = 'no'
                elif all(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
                    invoice_status = 'to invoice'
                elif all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
                    invoice_status = 'invoiced'
                elif all(invoice_status in ['invoiced', 'upselling'] for invoice_status in line_invoice_status):
                    invoice_status = 'upselling'
                else:
                    invoice_status = 'no'
            else:
                if order.state not in ('sale', 'done'):
                    invoice_status = 'no'
                elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
                    invoice_status = 'to invoice'
                elif all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
                    invoice_status = 'invoiced'
                elif all(invoice_status in ['invoiced', 'upselling'] for invoice_status in line_invoice_status):
                    invoice_status = 'upselling'
                else:
                    invoice_status = 'no'

            order.update({
                'invoice_count': len(set(invoice_ids.ids + refund_ids.ids)),
                'invoice_ids': invoice_ids.ids + refund_ids.ids,
                'invoice_status': invoice_status
            })

class PO(models.Model):
    _inherit = 'purchase.order'

    ssi_job_id = fields.Many2one('ssi_jobs', string='Job')

    @api.onchange('ssi_job_id')
    def _onchange_ssi_job_id(self):
        # When updating jobs dropdown, auto set analytic account on po lines.
        if self.ssi_job_id.aa_id:
            for line in self.order_line:
                line.account_analytic_id = self.ssi_job_id.aa_id
    