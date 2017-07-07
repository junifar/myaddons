
from openerp import models, api, fields

class Employee(models.Model):
	_inherit = "hr.employee"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null")
	kejaksaan_negeri_id = fields.Many2one('court.kejaksaan_negeri', string="Kejaksaan Agung", ondelete="set null")