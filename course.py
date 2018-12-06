from odoo import models, fields, api

class course(models.Model):
	_name = 'academic.course'
	
	name = fields.Char(string='Name', size=100, required=True)
	description = fields.Text(string='Description')
	responsible_id = fields.Many2one('res.users', string='Responsible')
	session_ids = fields.One2many('academic.session','course_id',string='Sessions', ondelete="cascade")

