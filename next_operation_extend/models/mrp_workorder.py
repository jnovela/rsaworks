# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.tools import float_compare, float_round

class MrpWorkorder(models.Model):

	_inherit = 'mrp.workorder'

	custom_sequence = fields.Integer(string="Custom Sequence")

	@api.model
	def create(self,vals):
		#This method will update the custom sequence to the workorder's sequence.
		res = super(MrpWorkorder, self).create(vals)
		res.production_id.routing_id.calculate_custom_sequence()
		res.update({'custom_sequence': res.operation_id.custom_sequence})
		return res

	@api.multi
	def find_preceding_workorders(self,production_id):
		#Method will find work orders and returns them
		workorders = self.search([('production_id','=',production_id.id),('custom_sequence','<',self.custom_sequence)])
		if workorders:
			return workorders
		else:
			return False

	@api.multi
	def button_start(self):
		#Method will inherit and change the logic for that.
		self.production_id.routing_id.calculate_custom_sequence()
		if self.operation_id.is_all_precending_wo_complete == True and self.operation_id.custom_sequence > 1:
			workorders = self.find_preceding_workorders(self.production_id)
			if workorders:
				if any(workorder.state != 'done' for workorder in workorders):
					raise Warning(_('You can not process this work order, please finish preceding work order first!'))
		return super(MrpWorkorder,self).button_start()