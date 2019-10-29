# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class GrossMarginReport(models.Model):
    _name = "gross.margin.report"
    _description = "Gross Margin Report"
    _auto = False
    _rec_name = 'date'

    number = fields.Char('Invoice #', readonly=True)
    account_name = fields.Char('Account Name', readonly=True)
    date = fields.Date(readonly=True, string="Invoice Date")
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_qty = fields.Float(string='Product Quantity', readonly=True)
    uom_name = fields.Char(string='Reference Unit of Measure', readonly=True)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', oldname='payment_term', readonly=True)
    fiscal_position_id = fields.Many2one('account.fiscal.position', oldname='fiscal_position', string='Fiscal Position', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', string='Partner Company', help="Commercial Entity")
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    price_total = fields.Float(string='Untaxed Total', readonly=True)
    price_average = fields.Float(string='Average Price', readonly=True, group_operator="avg")
#     currency_rate = fields.Float(string='Currency Rate', readonly=True, group_operator="avg", groups="base.group_multi_currency")
    nbr = fields.Integer(string='Line Count', readonly=True)  # TDE FIXME master: rename into nbr_lines
    invoice_id = fields.Many2one('account.invoice', readonly=True)
    type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_refund', 'Customer Credit Note'),
        ('in_refund', 'Vendor Credit Note'),
        ], readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')
        ], string='Invoice Status', readonly=True)
    date_due = fields.Date(string='Due Date', readonly=True)
    account_id = fields.Many2one('account.account', string='Receivable/Payable Account', readonly=True, domain=[('deprecated', '=', False)])
    account_line_id = fields.Many2one('account.account', string='Revenue/Expense Account', readonly=True, domain=[('deprecated', '=', False)])
    residual = fields.Float(string='Due Amount', readonly=True)
    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account', groups="analytic.group_analytic_accounting")
    credit = fields.Float(string='Credit', readonly=True)
    debit = fields.Float(string='Debit', readonly=True)
    margin = fields.Float(string='Gross Margin', readonly=True)
    amount_total = fields.Float(string='Total', readonly=True)

    _order = 'date desc'

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total_company_signed', 'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position_id',
            'journal_id', 'number', 'partner_bank_id', 'partner_id', 'payment_term_id',
            'residual', 'state', 'type', 'user_id',
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uom_id', 'account_analytic_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    def _select(self):
        select_str = """
				SELECT aml.id AS id, ai.date_invoice AS date, ai.number as number, ail.product_id, 
                    ai.partner_id, ai.payment_term_id, ail.account_analytic_id, u2.name AS uom_name,
                    ai.currency_id, ai.journal_id, ai.fiscal_position_id, ai.user_id, ai.company_id,
                    1 AS nbr, ai.id AS invoice_id, ai.type, ai.state, pt.categ_id, ai.date_due, ai.account_id,
                    aa.name as account_name, aa.user_type_id as account_type, ail.account_id AS account_line_id, 
                    SUM(aml.debit) as debit, SUM(aml.credit) as credit,
                    SUM ((ail.quantity) / COALESCE(u.factor,1) * COALESCE(u2.factor,1)) AS product_qty,
                    SUM(ail.price_subtotal_signed) AS price_total,
                    SUM(credit - debit) AS margin,
                    SUM(ail.price_total) AS amount_total
        """
        return select_str

    def _from(self):
        from_str = """
                FROM account_move_line aml
                JOIN account_move am on aml.move_id = am.id
                JOIN account_account aa on aml.account_id = aa.id
                JOIN account_invoice ai ON ai.id = aml.invoice_id
                JOIN account_invoice_line ail ON ai.id = ail.invoice_id
                JOIN res_partner partner_ai ON ai.partner_id = partner_ai.id
                LEFT JOIN product_product pr ON pr.id = ail.product_id
                left JOIN product_template pt ON pt.id = pr.product_tmpl_id
                LEFT JOIN uom_uom u ON u.id = ail.uom_id
                LEFT JOIN uom_uom u2 ON u2.id = pt.uom_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
                GROUP BY aml.id, ail.product_id, ail.account_analytic_id, ai.date_invoice, ai.id,
                    ai.partner_id, ai.payment_term_id, u2.name, u2.id, ai.currency_id, ai.journal_id,
                    ai.fiscal_position_id, ai.user_id, ai.company_id, ai.id, ai.type, ai.state, pt.categ_id,
                    ai.date_due, ai.account_id, ail.account_id, ai.residual_company_signed,
                    ai.amount_total_company_signed, aa.name, aa.user_type_id
        """
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s %s WHERE aml.account_id IS NOT NULL AND aa.user_type_id IN (14, 16) %s
        )""" % (
                    self._table, self._select(), self._from(), self._group_by()))

#         self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
#             WITH currency_rate AS (%s)
#             %s
#             FROM (
#                 %s %s WHERE ail.account_id IS NOT NULL %s
#             ) AS sub
#             LEFT JOIN currency_rate cr ON
#                 (cr.currency_id = sub.currency_id AND
#                  cr.company_id = sub.company_id AND
#                  cr.date_start <= COALESCE(sub.date, NOW()) AND
#                  (cr.date_end IS NULL OR cr.date_end > COALESCE(sub.date, NOW())))
#         )""" % (
#                     self._table, self.env['res.currency']._select_companies_rates(),
#                     self._select(), self._sub_select(), self._from(), self._group_by()))

