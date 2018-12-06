from odoo import models, fields, api

class session(models.Model):
	_name = 'academic.session'

	course_id = fields.Many2one('academic.course', string='Course')
	instructor_id = fields.Many2one('res.partner', string='Instructor')
	name = fields.Char(string='Name', size=100, required=True)
	start_date = fields.Date(string='Start Date', required=True)
	duration = fields.Integer(string='Duration')
	seats = fields.Integer(string='Number of Seats')
	active = fields.Boolean(string='Is Active?')
	attendee_ids = fields.One2many('academic.attendee','session_id',string='Attendees', ondelete="cascade")

