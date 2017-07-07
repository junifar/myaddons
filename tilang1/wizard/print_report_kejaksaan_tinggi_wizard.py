from openerp import models, fields, api, _
from openerp.osv import orm
from openerp.exceptions import UserError
from datetime import datetime

class kejaksaan_tinggi_report_tilang_xls(orm.TransientModel):
	_name = 'kejaksaan.tinggi.report.tilang.xls'
	_description = 'Print report tilang in kejaksaan tinggi'

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null")
	from_date = fields.Date(string="Dari tanggal")
	to_date = fields.Date(string="Hingga tanggal")

	@api.multi
	def print_report(self):
		return {}

class kejaksaan_negeri_report_tilang_xls(orm.TransientModel):
	_name = "kejaksaan.negeri.report.tilang.xls"
	_description = "Print report tilang in kejaksaan negeri"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null")
	kejaksaan_negeri_id = fields.Many2one('court.kejaksaan_negeri', string="Kejaksaan Negeri", ondelete="set null")
	from_date = fields.Date(string="Dari tanggal")
	to_date = fields.Date(string="Hingga tanggal")

	@api.multi
	def print_report(self):
		return {}


# NOTE : REKAP TILANG
class data_tilang_harian(orm.TransientModel):
	_name = 'rekap.tilang.harian'
	_description = "Rekap Tilang Harian"

	kejaksaan_negeri_id = fields.Many2one('court.kejaksaan_negeri', string="Kejaksaan Negeri", ondelete="set null")
	date_filter = fields.Date(string="Tanggal Sidang")	

	def _print_report(self,data):
		records = self.env[data['model']].browse(data.get('ids',[]))
		return self.env['report'].with_context(landscape=True).get_action(records,'tilang.report_tilang_harian', data=data)

	@api.multi
	def check_report(self):
		self.ensure_one()
		if not self.kejaksaan_negeri_id or not self.date_filter:
			raise UserError(_("All fields must be filled"))

		data = {}
		data['ids'] = self.env.context.get('active_ids',[])
		data['model'] = self.env.context.get('active_model','ir.ui.menu')
		data['form'] = self.read(['kejaksaan_negeri_id','date_filter'])[0]
		return self._print_report(data)

# NOTE : FORM 1A
class rekap_tilang_kejati(orm.TransientModel):
	_name = "rekap.tilang.kejati"
	_description = "Rekap Tilang Kejati"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null", required=True)
	report_type = fields.Selection(selection=[('Bulanan', 'Bulanan'), ('Semester','Semester'), ('Tahunan', 'Tahunan')], required=True, string="Report Type", default="Bulanan")
	semester_filter = fields.Selection(selection=[('I','I'),('II','II')], string="Semester")
	month_filter = fields.Selection(selection=[
		(1, 'Januari'),
		(2, 'Februari'),
		(3, 'Maret'),
		(4, 'April'),
		(5, 'Mei'),
		(6, 'Juni'),
		(7, 'Juli'),
		(8, 'Agustus'),
		(9, 'September'),
		(10, 'Oktober'),
		(11, 'November'),
		(12, 'Desember')
		], string="Bulan")
	year_filter = fields.Integer(string="Tahun", default=datetime.now().year)

	def _print_report(self, data):
		records = self.env[data['model']].browse(data.get('ids',[]))
		# return {}
		return self.env['report'].with_context(landscape=True).get_action(records,'tilang.report_tilang_kejati', data=data)

	@api.multi
	def check_report(self):
		self.ensure_one()
		self_obj = self.env.context

		while True:
			try :
				int(self.year_filter)
				break
			except ValueError:
				raise UserError(_("Invalid year input"))

		data = {}
		data['ids'] = self_obj.get('active_ids', [])
		data['model'] = self_obj.get('active_model', 'ir.ui.menu')
		data['form'] = self.read(['kejaksaan_tinggi_id','report_type','semester_filter','month_filter','year_filter'])[0]
		return self._print_report(data)

class laporan_kehadiran(orm.TransientModel):
	_name = "laporan.kehadiran"
	_description = "Laporan Kehadiran"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null", required=True)
	report_type = fields.Selection(selection=[('Bulanan', 'Bulanan'), ('Semester','Semester'), ('Tahunan', 'Tahunan')], required=True, string="Report Type", default="Bulanan")
	semester_filter = fields.Selection(selection=[('I','I'),('II','II')], string="Semester")
	month_filter = fields.Selection(selection=[
		(1, 'Januari'),
		(2, 'Februari'),
		(3, 'Maret'),
		(4, 'April'),
		(5, 'Mei'),
		(6, 'Juni'),
		(7, 'Juli'),
		(8, 'Agustus'),
		(9, 'September'),
		(10, 'Oktober'),
		(11, 'November'),
		(12, 'Desember')
		], string="Bulan")
	year_filter = fields.Integer(string="Tahun", default=datetime.now().year)

	def _print_report(self, data):
		records = self.env[data['model']].browse(data.get('ids',[]))
		return self.env['report'].with_context(landscape=True).get_action(records,'tilang.laporan_kehadiran', data=data)

	@api.multi
	def check_report(self):
		self.ensure_one()
		self_obj = self.env.context

		data = {}
		data['ids'] = self_obj.get('active_ids', [])
		data['model'] = self_obj.get('active_model', 'ir.ui.menu')
		data['form'] = self.read(['kejaksaan_tinggi_id','report_type','semester_filter','month_filter','year_filter'])[0]

		return self._print_report(data)

class laporan_barang_bukti(orm.TransientModel):
	_name = "laporan.barang.bukti"
	_description = "Laporan Barang Bukti"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null", required=True)
	report_type = fields.Selection(selection=[('Bulanan', 'Bulanan'), ('Semester','Semester'), ('Tahunan', 'Tahunan')], required=True, string="Report Type", default="Bulanan")
	semester_filter = fields.Selection(selection=[('I','I'),('II','II')], string="Semester")
	month_filter = fields.Selection(selection=[
		(1, 'Januari'),
		(2, 'Februari'),
		(3, 'Maret'),
		(4, 'April'),
		(5, 'Mei'),
		(6, 'Juni'),
		(7, 'Juli'),
		(8, 'Agustus'),
		(9, 'September'),
		(10, 'Oktober'),
		(11, 'November'),
		(12, 'Desember')
		], string="Bulan")
	year_filter = fields.Integer(string="Tahun", default=datetime.now().year)

	def _print_report(self, data):
		records = self.env[data['model']].browse(data.get('ids',[]))
		# return {}
		return self.env['report'].with_context(landscape=True).get_action(records,'tilang.laporan_barang_bukti', data=data)

	@api.multi
	def check_report(self):
		self.ensure_one()
		self_obj = self.env.context

		data = {}
		data['ids'] = self_obj.get('active_ids', [])
		data['model'] = self_obj.get('active_model', 'ir.ui.menu')
		data['form'] = self.read(['kejaksaan_tinggi_id','report_type','semester_filter','month_filter','year_filter'])[0]

		return self._print_report(data)

class laporan_giro(orm.TransientModel):
	_name = "laporan.giro"
	_description = "Laporan GIRO"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null", required=True)
	report_type = fields.Selection(selection=[('Bulanan', 'Bulanan'), ('Semester','Semester'), ('Tahunan', 'Tahunan')], required=True, string="Report Type", default="Bulanan")
	semester_filter = fields.Selection(selection=[('I','I'),('II','II')], string="Semester")
	month_filter = fields.Selection(selection=[
		(1, 'Januari'),
		(2, 'Februari'),
		(3, 'Maret'),
		(4, 'April'),
		(5, 'Mei'),
		(6, 'Juni'),
		(7, 'Juli'),
		(8, 'Agustus'),
		(9, 'September'),
		(10, 'Oktober'),
		(11, 'November'),
		(12, 'Desember')
		], string="Bulan")
	year_filter = fields.Integer(string="Tahun", default=datetime.now().year)

	def _print_report(self, data):
		records = self.env[data['model']].browse(data.get('ids',[]))
		# return {}
		return self.env['report'].with_context(landscape=True).get_action(records,'tilang.laporan_giro', data=data)

	@api.multi
	def check_report(self):
		self.ensure_one()
		self_obj = self.env.context

		data = {}
		data['ids'] = self_obj.get('active_ids', [])
		data['model'] = self_obj.get('active_model', 'ir.ui.menu')
		data['form'] = self.read(['kejaksaan_tinggi_id','report_type','semester_filter','month_filter','year_filter'])[0]

		return self._print_report(data)

class laporan_verstek(orm.TransientModel):
	_name = "laporan.verstek"
	_description = "Laporan Verstek"

	kejaksaan_tinggi_id = fields.Many2one('court.kejaksaan_tinggi', string="Kejaksaan Tinggi", ondelete="set null", required=True)
	report_type = fields.Selection(selection=[('Bulanan', 'Bulanan'), ('Semester','Semester'), ('Tahunan', 'Tahunan')], required=True, string="Report Type", default="Bulanan")
	semester_filter = fields.Selection(selection=[('I','I'),('II','II')], string="Semester")
	month_filter = fields.Selection(selection=[
		(1, 'Januari'),
		(2, 'Februari'),
		(3, 'Maret'),
		(4, 'April'),
		(5, 'Mei'),
		(6, 'Juni'),
		(7, 'Juli'),
		(8, 'Agustus'),
		(9, 'September'),
		(10, 'Oktober'),
		(11, 'November'),
		(12, 'Desember')
		], string="Bulan")
	year_filter = fields.Integer(string="Tahun", default=datetime.now().year)

	def _print_report(self, data):
		records = self.env[data['model']].browse(data.get('ids',[]))
		# return {}
		return self.env['report'].with_context(landscape=True).get_action(records,'tilang.laporan_verstek', data=data)
		# return self.env['report'].get_action(records,'tilang.laporan_verstek', data=data)

	@api.multi
	def check_report(self):
		self.ensure_one()
		self_obj = self.env.context

		data = {}
		data['ids'] = self_obj.get('active_ids', [])
		data['model'] = self_obj.get('active_model', 'ir.ui.menu')
		data['form'] = self.read(['kejaksaan_tinggi_id','report_type','semester_filter','month_filter','year_filter'])[0]

		return self._print_report(data)