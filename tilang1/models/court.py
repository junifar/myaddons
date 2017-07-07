from openerp import models, fields, api, _
from openerp.exceptions import UserError

class KejaksaanTinggi(models.Model):
	_name = "court.kejaksaan_tinggi"

	name = fields.Char(required=True, string="Kejaksaan tinggi")
	kejaksaan_negeri_ids = fields.One2many('court.kejaksaan_negeri','kejaksaan_tinggi_id', string="List Kejaksaan Negeri")
	case_ids = fields.One2many('court.case', 'kejaksaan_negeri_id', string="List kasus tilang")

	@api.multi
	def export_case(self, context=None):
		case_ids = {}
		datas={'ids':[self.id]}

		lines = []
		for data in self.case_ids:
			print '=====court_01====='
			print repr(data)
			print '=================='
			data_body = {
				'nama_terdakwa' : data['nama_terdakwa'],
				'nomor_tilang' : data['nomor_tilang'],
				'kejaksaan_negeri' : data['kejaksaan_negeri_id']['name'],
				'tanggal_tilang' : data['tanggal_tilang'],
				'denda' : data['denda'],
				'state' : data['state'],
				}
			lines.append(data_body)

		datas['lines'] = lines

		return {
			'type' : 'ir.actions.report.xml',
			'report_name' : 'case.list.xls',
			'datas' : datas,
		}

class KejaksaanNegeri(models.Model):
	_name = "court.kejaksaan_negeri"

	name = fields.Char(required=True, string="Kejaksaan Negeri")
	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null")
	case_ids = fields.One2many('court.case', 'kejaksaan_negeri_id', string="List kasus tilang")

class Case(models.Model):
	_name = "court.case"

	_rec_name = "nomor_tilang"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null")
	kejaksaan_negeri_id = fields.Many2one('court.kejaksaan_negeri', string="Kejaksaan Negeri", ondelete="set null")
	nomor_tilang = fields.Char(string="Nomor Surat Tilang")
	tanggal_tilang = fields.Date(string="Tanggal Tilang")
	nama_terdakwa = fields.Char(string="Nama Terdakwa / Terpidana")
	alamat_terdakwa = fields.Text(string="Alamat Terdakwa")
	pasal = fields.Char(string="Pasal yang Dilanggar")
	barang_bukti_type = fields.Selection(selection=[('SIM','SIM'),('STNK','STNK'),('MOTOR','Motor'),('MOBIL','Mobil')], string="Barang Bukti")
	barang_bukti = fields.Char(string="Barang Bukti")
	warna_surat_tilang = fields.Selection(selection=[('merah', 'Merah'), ('biru', 'Biru')])
	uang_titipan = fields.Integer(string="Uang Titipan (Giro I)")
	biaya_perkara = fields.Integer(string="Biaya Perkara", default=1000)
	denda = fields.Integer(string="Denda")
	bank = fields.Char(string="Alamat BRI / Pos dan Giro")
	tanggal_entry = fields.Date(string="Tanggal Registrasi Perkara", default=fields.Date.today)
	tanggal_putusan = fields.Date(string="Tanggal Putusan", default=fields.Date.today)
	no_putusan = fields.Char(string="No Putusan")
	status_kehadiran = fields.Selection(selection=[('hadir','Hadir'),('verstek','Verstek')], string="Hadir Sidang")
	status_hadir_kejaksaan = fields.Selection(selection=[('hadir','Hadir'),('tidak hadir','Tidak Hadir')], string="Hadir Kejaksaan")
	subsidair = fields.Char(string="Subsidair")
	status_pengembalian_barang_bukti = fields.Boolean(string="Pengembalian Barang Bukti")
	tanggal_pengembalian_barang_bukti = fields.Date(string="Tanggal Pengembalian")
	no_setoran_ke_kas_negara = fields.Char(string="No Setoran")
	tgl_setoran_ke_kas_negara = fields.Date(string="Tanggal Setoran")
	legas = fields.Char(string="Legas")
	remark = fields.Text(string="Keterangan")
	jumlah_bayar = fields.Integer(string="Jumlah Bayar (Giro II)", compute="_compute_jumlah_bayar", store=True)
	selisih_uang_titipan = fields.Integer(string="Selisih Uang Titipan (Giro III)", compute="_compute_selisih_uang_titipan", store=True)
	metode_pembayaran = fields.Selection(selection=[('CASH','Cash'),('TRANSFER','Transfer')])
	state = fields.Selection([
        ('berkas tilang', 'Berkas Tilang'),
        ('sidang','Sidang'),
        ('setoran ke negara', 'Setoran ke Negara'),
        ('pengembalian barang bukti', 'Pengembalian Barang Bukti'),
        ('arsip', 'Arsip'),
    ], string="Status")

	@api.multi
	def action_sidang(self):
		# if not self.env.user.jabatan == "staff kejari":
		# 	raise UserError(_("Akses di tolak"))
		self.state = 'sidang'

	@api.multi
	def action_berkas_tilang(self):
		# if not self.env.user.jabatan == "staff kejari":
		# 	raise UserError(_("Akses di tolak"))
		self.state = 'berkas tilang'

	@api.multi
	def action_setoran_ke_negara(self):
		# if not self.env.user.jabatan == "staff pengadilan":
		# 	raise UserError(_("Akses di tolak"))
		self.state = 'setoran ke negara'

	@api.multi
	def action_pengembalian_barang_bukti(self):
		# if not self.env.user.jabatan == "staff administrasi":
		# 	raise UserError(_("Akses di tolak"))
		self.state = 'pengembalian barang bukti'

	@api.multi
	def action_arsip(self):
		# if not self.env.user.jabatan == "staff pengembalian barang bukti":
		# 	raise UserError(_("Akses di tolak"))
		self.state = 'arsip'

	@api.multi
	def export_case(self, context=None):

		datas={'ids': [(self.id)]}
		datas['sample'] = self

		print '============'
		print datas
		print '============'

		# move_obj = self.pool.get('court.case')
		# cari = self.search_read([], ['nama_terdakwa'])

		return {
			'type' : 'ir.actions.report.xml',
			'report_name' : 'case.list.xls',
			'datas' : datas,
		}

	@api.depends('biaya_perkara','denda')
	def _compute_jumlah_bayar(self):
		self.jumlah_bayar = self.biaya_perkara + self.denda

	@api.depends('biaya_perkara','denda','uang_titipan')
	def _compute_selisih_uang_titipan(self):
		selisih_uang_titipan = self.uang_titipan - (self.biaya_perkara + self.denda)
		if  selisih_uang_titipan > 1 :
			self.selisih_uang_titipan = selisih_uang_titipan
		else :
			self.selisih_uang_titipan = 0

	@api.model
	def _report_xls_fields(self):
		return [
			'kejaksaan_negeri',
			'nama_terdakwa',
			'nomor_tilang',
			'tanggal_tilang',
			'denda',
			'state',
			]

    # Change/Add Template entries
	@api.model
	def _report_xls_template(self):
		"""
        Template updates, e.g.

        my_change = {
            'move':{
                'header': [1, 20, 'text', _('My Move Title')],
                'lines': [1, 0, 'text', _render("line.move_id.name or ''")],
                'totals': [1, 0, 'text', None]},
        }
        return my_change
        """
		return {}

	@property
	def __str__(self):
		return self.nomor_tilang