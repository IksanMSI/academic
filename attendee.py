from odoo import models, fields, api

class attendee(models.Model):
	_name = 'academic.attendee'

	session_id = fields.Many2one('academic.session', string='Session')
	partner_id = fields.Many2one('res.partner',string='Partner')
	name = fields.Char(string='Name', size=100)

