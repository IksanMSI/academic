from odoo import models, fields, api

class partner(models.Model):
	_name 		= 'res.partner'
	_inherit	= 'res.partner'

	is_instructor = fields.Boolean(string='Is Instructor')

