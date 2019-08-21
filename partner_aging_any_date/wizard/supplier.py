# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models, _


class SupplierAgingDate(models.TransientModel):
    _name = "supplier.aging.date"
    _description = 'Supplier Aging Date'

    age_date = fields.Datetime(
                        "Aging Date",
                        required=True,
                        default=lambda self: fields.Datetime.now())

    @api.multi
    def open_partner_aging(self):
        ctx = self._context.copy()
        age_date = self.age_date
        ctx.update({'age_date': age_date})

        supplier_aging = self.env['partner.aging.supplier.ad']

        query = """
                SELECT
                 aml.id,
                 aml.partner_id as partner_id,
                 ai.user_id as salesman,
                 aml.date as date,
                 aml.date as date_due,
                 ai.number as invoice_ref,
                days_due AS avg_days_overdue,
                CASE WHEN (days_due <= 0) THEN
                        CASE WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual<0) THEN aml.credit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date <= '%s')
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-\
                        (select coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date <= '%s'))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) \
                        THEN aml.amount_residual END ELSE 0 \
                        END AS not_due,
                CASE WHEN (days_due BETWEEN 1 and 30) THEN
                    CASE WHEN
                    (aml.full_reconcile_id is NULL and \
                    aml.amount_residual<0) THEN aml.credit-(select \
                    coalesce(sum(apr.amount),0) \
                    from account_partial_reconcile apr where \
                    (apr.credit_move_id =aml.id or apr.debit_move_id=aml.id)\
                     and apr.create_date <= '%s')
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select\
                         coalesce(sum(apr.amount),0) from \
                         account_partial_reconcile apr where \
                         (apr.credit_move_id =aml.id or \
                         apr.debit_move_id=aml.id) and \
                         apr.create_date <= '%s'))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS \
                        days_due_01to30,
                CASE WHEN (days_due BETWEEN 31 and 60) THEN
                    CASE WHEN
                    (aml.full_reconcile_id is NULL and \
                    aml.amount_residual<0) THEN aml.credit-(select \
                    coalesce(sum(apr.amount),0) \
                    from account_partial_reconcile apr where \
                    (apr.credit_move_id =aml.id or apr.debit_move_id=aml.id)\
                     and apr.create_date <= '%s')
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select\
                         coalesce(sum(apr.amount),0) from \
                         account_partial_reconcile apr where \
                         (apr.credit_move_id =aml.id or \
                         apr.debit_move_id=aml.id) and \
                         apr.create_date <= '%s'))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS \
                        days_due_31to60,
                CASE WHEN (days_due BETWEEN 61 and 90) THEN
                    CASE WHEN
                    (aml.full_reconcile_id is NULL and \
                    aml.amount_residual<0) THEN aml.credit-(select \
                    coalesce(sum(apr.amount),0) from \
                    account_partial_reconcile apr where \
                    (apr.credit_move_id =aml.id or apr.debit_move_id=aml.id)\
                     and apr.create_date <= '%s')
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select\
                         coalesce(sum(apr.amount),0) \
                         from account_partial_reconcile apr where \
                         (apr.credit_move_id =aml.id or \
                         apr.debit_move_id=aml.id) and \
                         apr.create_date <= '%s'))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS days_due_61to90,
                CASE WHEN (days_due BETWEEN 91 and 120) THEN
                        CASE WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual<0) THEN aml.credit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id \
                        =aml.id or apr.debit_move_id=aml.id) and \
                        apr.create_date <= '%s')
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or apr.debit_move_id\
                        =aml.id) and apr.create_date <= '%s'))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS \
                        days_due_91to120,
                CASE WHEN (days_due >= 121) THEN
                        CASE WHEN
                        (aml.full_reconcile_id is NULL and\
                         aml.amount_residual<0) THEN aml.credit-(select\
                          coalesce(sum(apr.amount),0) \
                          from account_partial_reconcile apr \
                          where (apr.credit_move_id =aml.id or \
                          apr.debit_move_id=aml.id) and apr.create_date \
                          <= '%s')
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select \
                        coalesce(sum(apr.amount),0) \
                        from account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) \
                        and apr.create_date <= '%s'))
                        WHEN (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS days_due_121togr,
                CASE when days_due < 0 THEN 0 ELSE days_due END as \
                "max_days_overdue",
                CASE WHEN
                (aml.full_reconcile_id is NULL and \
                aml.amount_residual<0) THEN aml.credit-(select \
                coalesce(sum(apr.amount),0) from account_partial_reconcile apr\
                 where (apr.credit_move_id =aml.id or apr.debit_move_id=aml.id)
                 and apr.create_date <= '%s')
                    WHEN
                    (aml.full_reconcile_id is NULL and aml.amount_residual>0) \
                    THEN -(aml.debit-(select coalesce(sum(apr.amount),0) from\
                     account_partial_reconcile apr where (apr.credit_move_id \
                     =aml.id or apr.debit_move_id=aml.id) and \
                     apr.create_date <= '%s'))
                     WHEN
                     (aml.full_reconcile_id is NOT NULL) THEN \
                     aml.amount_residual END AS total,
                ai.id as invoice_id,
                ai.date_due as inv_date_due
                FROM account_move_line aml
                INNER JOIN
                  (
                   SELECT lt.id,
                   CASE WHEN inv.date_due is null then CASE WHEN lt.date is not null THEN current_date - lt.date ELSE 0 END
                   WHEN inv.id is not null THEN '%s' - inv.date_due
                   ELSE current_date - lt.date END AS days_due
                   FROM account_move_line lt LEFT JOIN account_invoice inv on \
                   lt.move_id = inv.move_id
                ) DaysDue
                ON DaysDue.id = aml.id
                LEFT JOIN account_invoice as ai ON ai.move_id = \
                aml.move_id
                WHERE
                aml.user_type_id in (select id from account_account_type \
                where type = 'payable')
                and aml.date <='%s'
                and aml.amount_residual!=0
                GROUP BY aml.partner_id, aml.id, ai.number, days_due, \
                ai.user_id, ai.id
              """ % (age_date, age_date, age_date, age_date, age_date,\
                     age_date, age_date, age_date, age_date, age_date,\
                     age_date, age_date, age_date, age_date, age_date,\
                     age_date)

        tools.drop_view_if_exists(self.env.cr, '%s' % (\
                                    supplier_aging._name.replace('.', '_')))
        self.env.cr.execute("""
                      CREATE OR REPLACE VIEW %s AS ( %s)
        """ % (supplier_aging._name.replace('.', '_'), query))

        return {
              'name': _('Supplier Aging'),
              'view_type': 'form',
              "view_mode": 'tree,form',
              'res_model': 'partner.aging.supplier.ad',
              'type': 'ir.actions.act_window',
              'domain': [('total', '!=', 0)],
              'context': ctx,
        }


class PartnerAgingSupplierAD(models.Model):
    _name = 'partner.aging.supplier.ad'
    _description = 'Partner Aging Supplier Ad'
    _auto = False
    _order = 'partner_id'
    _rec_name = 'partner_id'

    @api.multi
    def invopen(self):
        """
            @description  Create link to view each listed invoice
        """
        view = self.env['ir.model.data'].xmlid_to_object(
                                                'account.invoice_form')
        view_id = view and view.id or False
        return {
            'name': ('Supplier Invoices'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view_id],
            'res_model': 'account.invoice',
            'context': "{'type':'in_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': self.invoice_id.id,
        }

    partner_id = fields.Many2one(
                            'res.partner',
                            u'Partner',
                            readonly=True)
    max_days_overdue = fields.Integer(
                            u'Days Outstanding',
                            readonly=True)
    avg_days_overdue = fields.Integer(
                            u'Avg Days Overdue',
                            readonly=True)
    date = fields.Date(
                    u'Date',
                    readonly=True)
    date_due = fields.Date(
                        u'Due Date',
                        readonly=True)
    inv_date_due = fields.Date(
                            u'Invoice Date',
                            readonly=True)
    total = fields.Float(
                    u'Total',
                    readonly=True)
    not_due = fields.Float(
                    u'Not Due Yet',
                    readonly=True)
    days_due_01to30 = fields.Float(
                            u'1/30',
                            readonly=True)
    days_due_31to60 = fields.Float(
                            u'31/60',
                            readonly=True)
    days_due_61to90 = fields.Float(
                            u'61/90',
                            readonly=True)
    days_due_91to120 = fields.Float(
                            u'91/120',
                            readonly=True)
    days_due_121togr = fields.Float(
                            u'+121',
                            readonly=True)
    invoice_ref = fields.Char(
                            'Their Invoice',
                            size=25,
                            readonly=True)
    invoice_id = fields.Many2one(
                                'account.invoice',
                                'Invoice',
                                readonly=True)

    @api.model_cr
    def init(self):
        cr = self._cr
        query = """
                SELECT
                aml.id,
                aml.partner_id as partner_id,
                ai.user_id as salesman,
                aml.date as date,
                aml.date as date_due,
                ai.number as invoice_ref,
                days_due AS avg_days_overdue,
                0 as days_due_01to30,
                CASE WHEN (days_due BETWEEN 31 and 60) THEN
                    CASE WHEN
                    (aml.full_reconcile_id is NULL and \
                    aml.amount_residual<0) THEN aml.credit-(select \
                    coalesce(sum(apr.amount),0) \
                    from account_partial_reconcile apr where \
                    (apr.credit_move_id =aml.id or apr.debit_move_id=aml.id) \
                    and apr.create_date <= current_date)
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select \
                        coalesce(sum(apr.amount),0) \
                        from account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or apr.debit_move_id\
                        =aml.id) and apr.create_date <= current_date))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS days_due_31to60,
                CASE WHEN (days_due BETWEEN 61 and 90) THEN
                    CASE WHEN
                    (aml.full_reconcile_id is NULL and aml.amount_residual<0) \
                    THEN aml.credit-(select coalesce(sum(apr.amount),0) from \
                    account_partial_reconcile apr where (apr.credit_move_id \
                    =aml.id or apr.debit_move_id=aml.id) and apr.create_date \
                    <= current_date)
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date <= \
                        current_date))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS \
                        days_due_61to90,
                CASE WHEN (days_due BETWEEN 91 and 120) THEN
                        CASE WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual<0) THEN aml.credit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date \
                        <= current_date)
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date <= \
                        current_date))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS days_due_91to120,
                CASE WHEN (days_due >= 121) THEN
                        CASE WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual<0) THEN aml.credit-(select \
                        coalesce(sum(apr.amount),0) \
                        from account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date \
                        <= current_date)
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and \
                        apr.create_date <= current_date))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS days_due_121togr,
                CASE when days_due < 0 THEN 0 ELSE days_due END as \
                "max_days_overdue",
                CASE WHEN (days_due < 31) THEN
                        CASE WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual<0) THEN aml.credit-(select \
                        coalesce(sum(apr.amount),0) \
                        from account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date \
                        <= current_date)
                        WHEN
                        (aml.full_reconcile_id is NULL and \
                        aml.amount_residual>0) THEN -(aml.debit-(select \
                        coalesce(sum(apr.amount),0) from \
                        account_partial_reconcile apr where \
                        (apr.credit_move_id =aml.id or \
                        apr.debit_move_id=aml.id) and apr.create_date \
                        <= current_date))
                        WHEN
                        (aml.full_reconcile_id is NOT NULL) THEN \
                        aml.amount_residual END ELSE 0 END AS not_due,
                CASE WHEN (aml.full_reconcile_id is NULL and \
                aml.amount_residual<0) THEN aml.credit-(select\
                 coalesce(sum(apr.amount),0) from \
                 account_partial_reconcile apr where (apr.credit_move_id \
                 =aml.id or apr.debit_move_id=aml.id) and \
                 apr.create_date <= current_date)
                    WHEN
                    (aml.full_reconcile_id is NULL and \
                    aml.amount_residual>0) THEN -(aml.debit-(select \
                    coalesce(sum(apr.amount),0) from \
                    account_partial_reconcile apr where \
                    (apr.credit_move_id =aml.id or apr.debit_move_id=aml.id) \
                    and apr.create_date <= current_date))
                     WHEN
                     (aml.full_reconcile_id is NOT NULL) THEN \
                     aml.amount_residual END AS total,
                ai.id as invoice_id,
                ai.date_due as inv_date_due
                FROM account_move_line aml
                INNER JOIN
                  (
                   SELECT lt.id,
                   CASE WHEN
                   inv.date_due is null then CASE WHEN lt.date is not null THEN current_date - lt.date ELSE 0 END
                   WHEN inv.id is not null THEN current_date - inv.date_due
                   ELSE current_date - lt.date END AS days_due
                   FROM account_move_line lt LEFT JOIN account_invoice inv on\
                    lt.move_id = inv.move_id
                ) DaysDue
                ON DaysDue.id = aml.id
                LEFT JOIN account_invoice as ai ON ai.move_id = aml.move_id
                WHERE
                aml.user_type_id in (select id from account_account_type \
                where type = 'payable')
                and aml.date <=current_date
                and aml.amount_residual!=0
                GROUP BY aml.partner_id, aml.id, ai.number, days_due,\
                 ai.user_id, ai.id
              """

        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))
        cr.execute("""
                      CREATE OR REPLACE VIEW %s AS ( %s)
        """ % (self._name.replace('.', '_'), query))