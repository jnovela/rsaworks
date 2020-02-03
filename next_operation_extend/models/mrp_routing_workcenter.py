# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class MrpRouting(models.Model):

	_inherit = 'mrp.routing'

	@api.multi
	def calculate_custom_sequence(self):
		#Calculates custom sequence
		sequence = 0
		if self.operation_ids:
			for operation in self.operation_ids:
				operation.write({'custom_sequence': sequence + 1})
				sequence += 1

class MrpRoutingWorkcenter(models.Model):

    _inherit = 'mrp.routing.workcenter'

    is_all_precending_wo_complete = fields.Boolean('Is All Preceding WO Complete',default=False,copy=False)
    custom_sequence = fields.Integer('Custom Sequence',copy=False)