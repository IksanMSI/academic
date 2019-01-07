from odoo import models, fields, api

class attendee(models.Model):
	_name = 'academic.attendee'

	session_id = fields.Many2one('academic.session', string='Session')
	partner_id = fields.Many2one('res.partner',string='Partner')
	name = fields.Char(string='Name', size=100)
	#course_id = fields.Related('session_id', 'course_id', type='many2one', relation='academic.course', string='Course', store=True)
	course_id = fields.Char(string='Course', store=True, related='session_id.course_id.name')

	_sql_constraints = [
		('partner_session_unique', 'CHECK(partner_id, session_id)', 'You cannot insert the same attendee multiple times!'),
		]