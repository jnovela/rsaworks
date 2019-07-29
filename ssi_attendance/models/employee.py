# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from random import choice
from string import digits
from odoo import models, fields, api, exceptions, _, SUPERUSER_ID
from odoo.exceptions import UserError


class HrEmployeeCustom(models.Model):
    _inherit = "hr.employee"

    @api.multi
    def attendance_manual(
            self,
            next_action,
            entered_pin=None,
            job=None,
            wo=None,
            lc=None,
            end=None):
        self.ensure_one()
        if not (entered_pin is None) or self.env['res.users'].browse(SUPERUSER_ID).has_group('hr_attendance.group_hr_attendance_use_pin') and (self.user_id and self.user_id.id != self._uid or not self.user_id):
            if entered_pin != self.pin:
                return {'warning': _('Wrong PIN')}

        if not (job is None) and not (wo is None):
            last_attendance = self.env['hr.attendance'].search(
                [('employee_id', '=', self.id)], limit=1)
            if last_attendance:
                now = fields.Datetime.now()
                last_attendance.sudo().write({'job_id': job})
                last_attendance.sudo().write({'workorder_id': wo})
                # last_attendance.sudo().write({'labor_code_id': lc})
                # raise UserError(_(str(end)))
                if end == 'false':
                    last_attendance.sudo().write(
                        {'check_out': now})

        return self.attendance_action(next_action)

    @api.multi
    def attendance_action(self, next_action):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        action_message = self.env.ref(
            'hr_attendance.hr_attendance_action_greeting_message').read()[0]
        action_message['previous_attendance_change_date'] = self.last_attendance_id and (
            self.last_attendance_id.check_out or self.last_attendance_id.check_in) or False
        action_message['employee_name'] = self.name
        action_message['barcode'] = self.barcode
        action_message['next_action'] = next_action

#         CUSTOM
        action_message['jobs'] = self.env['ssi_jobs'].search_read([])
        job_ids = []
        for job in action_message['jobs']:
            job_ids.append(job['id'])
        action_message['wos'] = self.env['mrp.workorder'].search_read(
            [('ssi_job_id', 'in', job_ids)])
        # action_message['lcs'] = self.env['x_labor.codes'].search_read([])

        if self.user_id:
            modified_attendance = self.sudo(
                self.user_id.id).attendance_action_change()
        else:
            modified_attendance = self.sudo().attendance_action_change()
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}
