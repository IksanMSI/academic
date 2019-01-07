from odoo import models, fields, api

SESSION_STATES = [('draft','Draft'),('confirmed','Confirmed'),('done','Done')]

class session(models.Model):
	_name = 'academic.session'

	#_defaults = {
	#	'start_date'	: lambda * a: time.strftime("%Y-%m-%d"),
	#	'active'		: True
	#}

	#def hitung(self, attendee_ids, seats):
	#	pct = 100.0 * len(attendee_ids) / seats
	#	return pct

	#def _calc_taken_seats(self, cr, uid, ids, field, arg, contex=None):
	#	results={}
	#	sessions = self.browse(cr, uid, ids, context=context)
	#	for session in sessions:
	#		if session.seats:
				#results[session.id] = 100.0 * len(session.attendee_ids) / session.seats
	#			results[session.id] = self.hitung(session.attendee_ids, session.seats)
	#		else:
	#			results[session.id] = 0.0

	#	return results
	
	#def onchange_seats(self, cr, uid, ids, seats, attendee_ids):
	#	array_of_attendees = self.resolve_o2m_commands_to_record_dicts(cr, uid, 'attendee_ids', attendee_ids, ['id'])

	#	results = {
	#		'value' : {
				#'taken_seats' : 100.0 * len(array_of_attendees) / seats
	#			'taken_seats' : self.hitung(array_of_attendees, seats)
	#		}
	#	}
		
		# kalau seats yang diinput < 0: warning message
	#	if seats < 0:
	#		results['warning'] = {
	#			'title'		: 'Warning: bad seats value',
	#			'message'	: 'Please enter a positive number'
	#		}
		# kalau seats yang diinput < jumlah attendee: warning message
	#	elif seats < len(array_of_attendees):
	#		results['warning'] = {
	#			'title'		: 'Warning: bad seats value',
	#			'message'	: 'Please enter more seats number'
	#		}

	#	return results

	# mau cek apakah intruktur_id ada di dalam attendee_ids.partner.id
	#def _cek_instruktur(self, cr, uid, ids, context=None):
	#	sessions = self.browse(cr, uid, ids, context=context)

	#	for session in sessions:
	#		x = [att.partner_id.id for att in session.attendee_ids]
	#		if session.instructor_id.id in x:
	#			return False

	#	return True

	#_constraints = [(_cek_instruktur, 'Instructor cannot be Attendee', ['instructor_id', 'attendee_ids'])]

	course_id = fields.Many2one('academic.course', string='Course', required=True)
	instructor_id = fields.Many2one('res.partner', string='Instructor')
	name = fields.Char(string='Name', size=100, required=True)
	start_date = fields.Date(string='Start Date', default=fields.Date.today, required=True)
	duration = fields.Integer(string='Duration')
	seats = fields.Integer(string='Number of Seats')
	active = fields.Boolean(string='Is Active?', default=True)
	attendee_ids = fields.One2many('academic.attendee','session_id',string='Attendees', ondelete="cascade")
	#taken_seats = fields.function(_calc_taken_seats, type='float', string='Taken Seats')
	taken_seats = fields.Float(string='Taken Seats', compute='_calc_taken_seats')
	image_small = fields.Binary(string='Image Small')
	state = fields.Selection(SESSION_STATES,string='Status',readonly=True,required=True, default=SESSION_STATES[0][0])

	@api.depends('seats', 'attendee_ids')
	def _calc_taken_seats(self):
		for r in self:
			if not r.seats:
				r.taken_seats = 0.0
			else:
				r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

	@api.onchange('seats', 'attendee_ids')
	def _onchange_seats(self):
		# kalau seats yang diinput < 0: warning message
		if self.seats < 0:
			return {
				'warning' : {
					'title'		: 'Warning: bad seats value',
					'message'	: 'Please enter a positive number'
				},
			}

		# kalau seats yang diinput < jumlah attendee: warning message
		if self.seats < len(self.attendee_ids):
			return {
				'warning' : {
					'title'		: 'Warning: bad seats value',
					'message'	: 'Please enter more seats number'
				},
			}

	#@api.constrains('instructor_id', 'attendee_ids')
	#def _cek_instruktur(self):
	#	for r in self:
	#		if r.attendee_ids:
	#			if r.instructor_id and r.instructor_id in r.attendee_ids:
	#				raise ValidationError("Instructor cannot be Attendee")

	#def copy(self, cr, uid, id, defaults, context=None)
	#	prev_session = self.browse(cr, uid, id, context=context)
	#	prev_name = prev_session.name
	#	defaults['name'] = 'Copy of %s' % prev_name
	#	new_session = super(session, self).copy(cr, uid, id, defaults, context=context)
	#	return new_session

	@api.one
	@api.returns('self', lambda value: value.id)
	def copy(self, default=None):
		default = dict(default or {})
		default.update({
	 		'name': 'Copy of %s' % (self.name),
		})
		return super(session, self).copy(default)

	@api.one
	def action_draft(self):
		#set to draft state
		return self.update({'state': SESSION_STATES[0][0]})

	@api.one
	def action_confirm(self):
		#set to confirm state
		return self.update({'state': SESSION_STATES[1][0]})

	@api.one
	def action_done(self):
		#set to done state
		return self.update({'state': SESSION_STATES[2][0]})

	_sql_constraints = [
		('name_description_check', 'CHECK(name <> description)', 'The title of the course should be different of the description'),
		('name_unique', 'UNIQUE(name)', 'The title must be unique')
		]
