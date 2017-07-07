from openerp import api, models

class ReportTilangHarian(models.AbstractModel):
	_name = 'report.tilang.report_tilang_harian'

	def _get_kejaksaan_negeri_name(self, data):
		lines = []
		kejaksaan_negeri_report = self.env['court.kejaksaan_negeri'].search([('id','=',data.get('kejaksaan_negeri_id')[0])])

		return kejaksaan_negeri_report.name

	def _get_case_list(self,data):
		case_obj = self.env['court.case']
		case_list = case_obj.search([('kejaksaan_negeri_id','=',data.get('kejaksaan_negeri_id')[0]),('tanggal_putusan','=',data.get('date_filter'))])
		# case_list = case_obj.search([('kejaksaan_negeri_id','=',data.get('kejaksaan_negeri_id')[0])])
		# print '=========================='
		# print repr(case_list)
		# print '=========================='
		return case_list


	@api.multi
	def render_html(self, data):
		self.model = self.env.context.get('active_model')
		docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
		# kejaksaan_negeri_name = data['form'].get('kejaksaan_negeri_id')[1]
		kejaksaan_negeri_name = self._get_kejaksaan_negeri_name(data.get('form'))
		case_lists = self._get_case_list(data.get('form'))

		docargs = {
			'doc_ids' : self.ids,
			'doc_model' : self.model,
			'data' : data['form'],
			'docs' : docs,
			'kejaksaan_negeri_name' : kejaksaan_negeri_name,
			'case_list' : case_lists,
		}
		return self.env['report'].render('tilang.report_tilang_harian', docargs)