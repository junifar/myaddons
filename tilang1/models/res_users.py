from openerp import models, api, fields

class Users(models.Model):
	_inherit = "res.users"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null")
	kejaksaan_negeri_id = fields.Many2one('court.kejaksaan_negeri', string="Kejaksaan Negeri", ondelete="set null")
	# jabatan = fields.Selection(selection=[
	# 	('staff kejari','Staff Kejari'),
	# 	('staff kejati','Staff Kejati'),
	# 	('staff pengadilan','Staff Pengadilan'),
	# 	('staff administrasi', 'Staff Administrasi'),
	# 	('staff pengembalian barang bukti', 'Staff Pengembalian Barang Bukti')], string="Jabatan")
	# fields.Text(string="kejari")
	# kejari_id = fields.Many2one('court.kejaksaan_negeri', string="Kejaksaan Negeri", ondelete="set null")
	