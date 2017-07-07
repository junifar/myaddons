from openerp import api, models

class LaporanGiro(models.AbstractModel):
	_name = 'report.tilang.laporan_giro'

	def _get_kejaksaan_tinggi_name(self, data):
		kejaksaan_tinggi_report = self.env['court.kejaksaan_tinggi'].search([('id','=',data.get('kejaksaan_tinggi_id')[0])])

		return kejaksaan_tinggi_report.name

	def query_tahunan(self,data):
		query = """
				SELECT
					"public".court_kejaksaan_negeri."name" AS kejaksaan_negeri_name,
					Count("public".court_kejaksaan_negeri."name") AS jumlah_perkara,
					COALESCE(SUM("public".court_case.uang_titipan),0) as uang_titipan,
					COALESCE(Sum("public".court_case.denda),0) AS denda,	
				    COALESCE(Sum("public".court_case.biaya_perkara),0) AS biaya_perkara,
					COALESCE(SUM("public".court_case.selisih_uang_titipan),0) as selisih_uang_titipan
				FROM
					"public".court_case
					LEFT JOIN "public".court_kejaksaan_negeri ON "public".court_case.kejaksaan_negeri_id = "public".court_kejaksaan_negeri."id"
				WHERE
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry) = """+ str(data.get('year_filter')) +""" AND
					"public".court_kejaksaan_negeri."name" IS NOT NULL
				GROUP BY
					"public".court_kejaksaan_negeri."name",
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry)
				"""
		return query

	def query_bulanan(self, data):
		query = """
				SELECT
					"public".court_kejaksaan_negeri."name" AS kejaksaan_negeri_name,
					Count("public".court_kejaksaan_negeri."name") AS jumlah_perkara,
					COALESCE(SUM("public".court_case.uang_titipan),0) as uang_titipan,
					COALESCE(Sum("public".court_case.denda),0) AS denda,	
				    COALESCE(Sum("public".court_case.biaya_perkara),0) AS biaya_perkara,
					COALESCE(SUM("public".court_case.selisih_uang_titipan),0) as selisih_uang_titipan
				FROM
					"public".court_case
					LEFT JOIN "public".court_kejaksaan_negeri ON "public".court_case.kejaksaan_negeri_id = "public".court_kejaksaan_negeri."id"
				WHERE
					EXTRACT(MONTH FROM "public".court_case.tanggal_entry) = """+ str(data.get('month_filter')) +""" AND
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry) = """+ str(data.get('year_filter')) +""" AND
					"public".court_kejaksaan_negeri."name" IS NOT NULL
				GROUP BY
					"public".court_kejaksaan_negeri."name",
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry)
				"""		
		return query

	def query_semester(self,data):
		query = None
		if data.get('semester_filter') == 'I' :
			query = """
				SELECT
					"public".court_kejaksaan_negeri."name" AS kejaksaan_negeri_name,
					Count("public".court_kejaksaan_negeri."name") AS jumlah_perkara,
					COALESCE(SUM("public".court_case.uang_titipan),0) as uang_titipan,
					COALESCE(Sum("public".court_case.denda),0) AS denda,	
				    COALESCE(Sum("public".court_case.biaya_perkara),0) AS biaya_perkara,
					COALESCE(SUM("public".court_case.selisih_uang_titipan),0) as selisih_uang_titipan
				FROM
					"public".court_case
					LEFT JOIN "public".court_kejaksaan_negeri ON "public".court_case.kejaksaan_negeri_id = "public".court_kejaksaan_negeri."id"
				WHERE
					EXTRACT(MONTH FROM "public".court_case.tanggal_entry) in (1,2,3,4,5,6) AND
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry) = """+ str(data.get('year_filter')) +""" AND
					"public".court_kejaksaan_negeri."name" IS NOT NULL
				GROUP BY
					"public".court_kejaksaan_negeri."name",
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry)
				"""			
		else :
			query = """
				SELECT
					"public".court_kejaksaan_negeri."name" AS kejaksaan_negeri_name,
					Count("public".court_kejaksaan_negeri."name") AS jumlah_perkara,
					COALESCE(SUM("public".court_case.uang_titipan),0) as uang_titipan,
					COALESCE(Sum("public".court_case.denda),0) AS denda,	
				    COALESCE(Sum("public".court_case.biaya_perkara),0) AS biaya_perkara,
					COALESCE(SUM("public".court_case.selisih_uang_titipan),0) as selisih_uang_titipan
				FROM
					"public".court_case
					LEFT JOIN "public".court_kejaksaan_negeri ON "public".court_case.kejaksaan_negeri_id = "public".court_kejaksaan_negeri."id"
				WHERE
					EXTRACT(MONTH FROM "public".court_case.tanggal_entry) in (7,8,9,10,11,12) AND
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry) = """+ str(data.get('year_filter')) +""" AND
					"public".court_kejaksaan_negeri."name" IS NOT NULL
				GROUP BY
					"public".court_kejaksaan_negeri."name",
					EXTRACT(YEAR FROM "public".court_case.tanggal_entry)
				"""			
		return query

	def _get_case_list(self, data):
		lines = []

		process_report = {
			'Tahunan' : self.query_tahunan(data),
           	'Semester' : self.query_semester(data),
           	'Bulanan' : self.query_bulanan(data)
           	}
		
		query = process_report[data.get('report_type')]
		self.env.cr.execute(query)
		res = self.env.cr.dictfetchall()
		for r in res :
			lines.append(r)
		return lines

	@api.multi
	def render_html(self,data):
		self.model = self.env.context.get('active_model')
		docs = self.env[self.model].browse(self.env.context.get('active_ids',[]))

		kejaksaan_tinggi_name = self._get_kejaksaan_tinggi_name(data.get('form'))
		case_list = self._get_case_list(data.get('form'))		

		docargs = {
			'doc_ids' : self.ids,
			'doc_model' : self.model,
			'data' : data['form'],
			'docs' : docs,
			'kejaksaan_tinggi_name' : kejaksaan_tinggi_name,
			'tahun_filter' : data.get('form').get('year_filter'),
			'case_list' : case_list,
			'report_type': data.get('form').get('report_type'),
			'semester_filter' : data.get('form').get('semester_filter'),
			'bulan_filter' : data.get('form').get('month_filter')
		}

		return self.env['report'].render('tilang.laporan_giro', docargs)