from odoo import models, fields, api

class session(models.Model):
	_name = 'academic.session'

	def hitung(self, attendee_ids, seats):
		pct = 100.0 * len(attendee_ids) / seats
		return pct

	def _calc_taken_seats(self, cr, uid, ids, field, arg, contex=None):
		results={}
		sessions = self.browse(cr, uid, ids, context=context)
		for session in sessions:
			if session.seats:
				#results[session.id] = 100.0 * len(session.attendee_ids) / session.seats
				results[session.id] = self.hitung(session.attendee_ids, session.seats)
			else:
				results[session.id] = 0.0

		return results
	
	def onchange_seats(self, cr, uid, ids, seats, attendee_ids):
		array_of_attendees = self.resolve_o2m_commands_to_record_dicts(cr, uid, 'attendee_ids', attendee_ids, ['id'])

		results = {
			'value' : {
				#'taken_seats' : 100.0 * len(array_of_attendees) / seats
				'taken_seats' : self.hitung(array_of_attendees, seats)
			}
		}
		
		# kalau seats yang diinput < 0: warning message
		if seats < 0:
			results['warning'] = {
				'title'		: 'Warning: bad seats value',
				'message'	: 'Please enter a positive number'
			}
		# kalau seats yang diinput < jumlah attendee: warning message
		elif seats < len(array_of_attendees):
			results['warning'] = {
				'title'		: 'Warning: bad seats value',
				'message'	: 'Please enter more seats number'
			}

		return results

	# mau cek apakah intruktur_id ada di dalam attendee_ids.partner.id
	def _cek_instruktur(self, cr, uid, ids, context=None):
		sessions = self.browse(cr, uid, ids, context=context)

		for session in sessions:
			x = [att.partner_id.id for att in session.attendee_ids]
			if session.instructor_id.id in x:
				return False

		return True

	_constraints = [(_cek_instruktur, 'Instructor cannot be Attendee', ['instructor_id', 'attendee_ids'])]

	course_id = fields.Many2one('academic.course', string='Course')
	instructor_id = fields.Many2one('res.partner', string='Instructor')
	name = fields.Char(string='Name', size=100, required=True)
	start_date = fields.Date(string='Start Date', required=True)
	duration = fields.Integer(string='Duration')
	seats = fields.Integer(string='Number of Seats')
	active = fields.Boolean(string='Is Active?')
	attendee_ids = fields.One2many('academic.attendee','session_id',string='Attendees', ondelete="cascade")
	taken_seats = fields.function(_calc_taken_seats, type='float', string='Taken Seats')

	_sql_constraints = [
		('name_description_check', 'CHECK(name <> description)', 'The title of the course should be different of the description'),
		('name_unique', 'UNIQUE(name)', 'The title must be unique'),
		]
