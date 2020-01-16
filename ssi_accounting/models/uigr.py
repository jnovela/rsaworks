# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
import json
from odoo import api, models, _
from odoo.tools.misc import formatLang, format_date
from odoo.exceptions import UserError
from odoo.addons.web.controllers.main import clean_action
from datetime import datetime, timedelta
from pytz import timezone, UTC


class ReportUigr(models.AbstractModel):
    _name = "account.report.uigr"
    _description = "UIGR Report"
    _inherit = 'account.report'

#     filter_date = {'date_from': '', 'date_to': '', 'filter': 'this_month'}
#     filter_unfold_all = True
#     filter_partner = True
    filter_date = {'date_from': '', 'filter': 'this_month'}
    filter_analytic = True

    def _get_columns_name(self, options):
        return [{'name': _('Vendor')},
            {'name': _('Vendor Name')},
            {'name': _('PO #')},
            {'name': _('Recv #')},
            {'name': _('Rec Date')},
            {'name': _('Received $'), 'class': 'number'},
            {'name': _('Invoiced $'), 'class': 'number'},
            {'name': _('Outstanding'), 'class': 'number'}
        ]

    @api.model
    def _get_lines(self, options, line_id=None):
        return self._get_lines_regular(options, line_id)

    @api.model
    def _get_lines_regular(self, options, line_id=None):
        lines = []
        tables, where_clause, where_params = self.env['account.move.line'].with_context(strict_range=True)._query_get()
#         user_type_id = self.env['account.account.type'].search([('type', '=', 'receivable')])
        if where_clause:
            where_clause = 'AND ' + where_clause
        # When unfolding, only fetch sum for the job we are unfolding and
        # fetch all partners for that country
        if line_id != None:
            if isinstance(line_id, int):
                where_clause = 'AND \"account_move_line\".analytic_account_id = %s ' + where_clause
                where_params = [line_id] + where_params
            else:
                where_clause = 'AND am.ref = %s ' + where_clause
                where_params = [line_id] + where_params

            unfold_query = """
                SELECT 
                    sum(\"account_move_line\".debit) FILTER (WHERE ac.group_id = 4) AS lab_debit, 
                    sum(\"account_move_line\".credit) FILTER (WHERE ac.group_id = 4) AS lab_credit,
                    sum(\"account_move_line\".debit) FILTER (WHERE ac.group_id = 5) AS mat_debit, 
                    sum(\"account_move_line\".credit) FILTER (WHERE ac.group_id = 5) AS mat_credit,
                    sum(\"account_move_line\".debit) FILTER (WHERE ac.group_id = 6) AS lab_a_debit, 
                    sum(\"account_move_line\".credit) FILTER (WHERE ac.group_id = 6) AS lab_a_credit,
                    sum(\"account_move_line\".debit) FILTER (WHERE ac.group_id = 7) AS mat_a_debit, 
                    sum(\"account_move_line\".credit) FILTER (WHERE ac.group_id = 7) AS mat_a_credit,
                    \"account_move_line\".analytic_account_id AS aa_id, MIN(\"account_move_line\".id) AS aml_id, pc.profit_center
                    FROM """+tables+"""
                    LEFT JOIN account_account ac on \"account_move_line\".account_id = ac.id
                    LEFT JOIN account_analytic_account aa on \"account_move_line\".analytic_account_id = aa.id
                    LEFT JOIN account_move am on \"account_move_line\".move_id = am.id
                    LEFT JOIN product_product pp on \"account_move_line\".product_id = pp.id
                    LEFT JOIN product_template pt on pp.product_tmpl_id = pt.id
                    LEFT JOIN product_category pc on pt.categ_id = pc.id
                    WHERE ac.group_id IN (4, 5) """+where_clause+"""
                    GROUP BY aa_id, pc.profit_center ORDER BY pc.profit_center
            """


#                 sum(\"account_move_line\".debit) FILTER (WHERE ac.group_id = 4 and \"account_move_line\".ref LIKE '%%Labor%%') AS lab_debit, 
#                 sum(\"account_move_line\".credit) FILTER (WHERE ac.group_id = 4 and \"account_move_line\".ref LIKE '%%Labor%%') AS lab_credit,
#                 sum(\"account_move_line\".debit) FILTER (WHERE ac.group_id = 4 and \"account_move_line\".ref LIKE '%%Burden%%') AS lab_b_debit, 
#                 sum(\"account_move_line\".credit) FILTER (WHERE ac.group_id = 4 and \"account_move_line\".ref LIKE '%%Burden%%') AS lab_b_credit,
        sql_query = """
            SELECT sum(\"account_move_line\".balance)*-1 AS balance, 
                sum(\"account_move_line\".credit)*-1 AS credit, 
                sum(\"account_move_line\".debit)*-1 AS debit, 
                \"account_move_line\".id AS aa_id, p.name as part_name, p.ref as part_ref,
                ai.date_invoice, ai.name as bill_name, ai.reference as bill_ref
                FROM """+tables+"""
                LEFT JOIN res_partner p ON \"account_move_line\".partner_id = p.id
                LEFT JOIN account_account ac on \"account_move_line\".account_id = ac.id
                LEFT JOIN account_move am on \"account_move_line\".move_id = am.id
                LEFT JOIN account_invoice ai on am.id = ai.move_id
                WHERE ac.code IN ('1211','1220','1221','1225') """+where_clause+"""
                GROUP BY \"account_move_line\".id, p.ref, p.name, ai.date_invoice, ai.name, ai.reference
        """

        params = where_params
        self.env.cr.execute(sql_query, params)
        results = self.env.cr.dictfetchall()

        total_c = 0
        total_d = 0
        total_b = 0
        for k, line in enumerate(results):
#                 order = self.env['sale.order'].search([('analytic_account_id', '=', line.get('aa_id'))], limit=1)
            partner_name = job.partner_id.parent_id.name and str(job.partner_id.parent_id.name) + ', ' + job.partner_id.name or job.partner_id.name
            if line.get('credit'):
                lines.append({
                    'id': id,
                    'name': line.get('part_ref'),
                    'level': 2,
                    'unfoldable': True,
                    'unfolded': line_id == id and True or False,
                    'columns': [{'name': line.get('part_name')}, 
                        {'name': line.get('bill_name')},
                        {'name': line.get('bill_ref')},
                        {'name': line.get('date_invoice')},
                        {'name': self.format_value(float(line.get('credit')))},
                        {'name': self.format_value(line.get('debit'))},
                        {'name': self.format_value(line.get('balance'))}
                     ],
                })
        # Adding profit center lines
#         if line_id:
#             self.env.cr.execute(unfold_query, params)
#             results = self.env.cr.dictfetchall()
#             for child_line in results:
#                 if not child_line.get('lab_credit'):
#                     child_line['lab_credit'] = 0 
#                 if not child_line.get('lab_debit'):
#                     child_line['lab_debit'] = 0 
#                 if not child_line.get('mat_credit'):
#                     child_line['mat_credit'] = 0 
#                 if not child_line.get('mat_debit'):
#                     child_line['mat_debit'] = 0 
#                 if not child_line.get('lab_a_credit'):
#                     child_line['lab_a_credit'] = 0 
#                 if not child_line.get('lab_a_debit'):
#                     child_line['lab_a_debit'] = 0 
#                 if not child_line.get('mat_a_credit'):
#                     child_line['mat_a_credit'] = 0 
#                 if not child_line.get('mat_a_debit'):
#                     child_line['mat_a_debit'] = 0 
#                 lines.append({
#                         'id': child_line.get('aa_id'),
#                         'name': child_line.get('profit_center'),
#                         'level': 4,
#                         'caret_options': '',
#                         'parent_id': line_id,
#                         'columns': [{'name': v} for v in [
#                             '', 
#                             '', 
#                             '', 
#                             '', 
#                             '', 
#                             '', 
#                             '', 
#                             '', 
#                             '', 
#                             self.format_value(child_line.get('lab_debit')-child_line.get('lab_credit')), 
# #                             self.format_value(child_line.get('lab_b_debit')-child_line.get('lab_b_credit')), 
#                             self.format_value(child_line.get('mat_debit')-child_line.get('mat_credit')),
#                             self.format_value(child_line.get('lab_a_debit')-child_line.get('lab_a_credit')),
#                             self.format_value(child_line.get('mat_a_debit')-child_line.get('mat_a_credit')),
#                         ]],
#                     })
#             # Sum of all the partner lines
#             lines.append({
#                     'id': 'total_%s' % (line_id,),
#                     'class': 'o_account_reports_domain_total',
#                     'name': _('Total '),
#                     'parent_id': line_id,
#                     'columns': [{'name': v} for v in ['', '', '', '', '', child_line.get('total_l')]],
#                 })

        # Don't display level 0 total line in case we are unfolding
        if total_l and not line_id:
            lines.append({
                'id': 'total',
                'name': _('Total'),
                'level': 0,
                'class': 'total',
                'columns': [{'name': v} for v in [
                        '', 
                        '',
                        '', 
                        '', 
                        '', 
                        '', 
                        '', 
                        '', 
                        '', 
                    ]],
                })
        return lines

    def _get_report_name(self):
        return _('UIGR Report')

    def _get_templates(self):
        templates = super(ReportUigr, self)._get_templates()
        templates['main_template'] = 'ssi_accounting.template_uigr_report'
        templates['line_template'] = 'ssi_accounting.line_template_uigr_report'
        return templates

    def open_analytic_entries(self, options, params):
        aa_id = params.get('aa_id')
        action = self.env.ref('analytic.account_analytic_line_action').read()[0]
        action = clean_action(action)
        action['context'] = {
            'active_id': aa_id,
        }
        return action

