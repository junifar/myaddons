import xlwt
from datetime import datetime
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _
import logging
_logger = logging.getLogger(__name__)

_ir_translation_name = 'case.list.xls'

class case_list_xls_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(move_line_xls_parser, self).__init__(
            cr, uid, name, context=context)
        move_obj = self.pool.get('court.case')
        self.context = context
        wanted_list = move_obj._report_xls_fields(cr, uid, context)
        template_changes = move_obj._report_xls_template(cr, uid, context)
        self.localcontext.update({
            'datetime': datetime,
            'wanted_list': wanted_list,
            'template_changes': template_changes,
            '_': self._,
        })

    def _(self, src):
        lang = self.context.get('lang', 'en_US')
        return translate(self.cr, _ir_translation_name, 'report', lang, src) \
            or src

class case_list_xls(report_xls):

	def __init__(self, name, table, rml=False, parser=False, header=True, store=False):
		super(case_list_xls, self).__init__(name, table, rml, parser, header, store)

		_xs = self.xls_styles

		rh_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
		self.rh_cell_style = xlwt.easyxf(rh_cell_format)
		self.rh_cell_style_center = xlwt.easyxf(rh_cell_format + _xs['center'])
		self.rh_cell_style_right = xlwt.easyxf(rh_cell_format + _xs['right'])

		aml_cell_format = _xs['borders_all']
		self.aml_cell_style = xlwt.easyxf(aml_cell_format)
		self.aml_cell_style_center = xlwt.easyxf(aml_cell_format + _xs['center'])
		self.aml_cell_style_date = xlwt.easyxf(aml_cell_format + _xs['left'], num_format_str=report_xls.date_format)
		self.aml_cell_style_decimal = xlwt.easyxf(aml_cell_format + _xs['right'], num_format_str=report_xls.decimal_format)

		rt_cell_format = _xs['bold'] + _xs['fill'] + _xs['borders_all']
		self.rt_cell_style = xlwt.easyxf(rt_cell_format)
		self.rt_cell_style_right = xlwt.easyxf(rt_cell_format + _xs['right'])
		self.rt_cell_style_decimal = xlwt.easyxf(rt_cell_format + _xs['right'], num_format_str=report_xls.decimal_format)

		self.col_specs_template = {
			'nama_terdakwa' : {
				'header' : [1, 42, 'text', _render("_('test')")],
				'lines' : [1, 0, 'text', _render("nama_terdakwa")],
				'totals' : [1, 0, 'text', None]
			},
		}

	def generate_xls_report(self, _p, _xs, data, objects, wb):

		wanted_list = _p.wanted_list
		self.col_specs_template.update(_p.template_changes)
		_ = _p._

		report_name = _("Contoh")
		ws = wb.add_shet(report_name[:31])
		ws.panes_frozen = True
		ws.remove_splits = True
		ws.potrait = 0
		ws.fit_width_to_pages = 1
		row_pos = 0

		ws.header_str = self.xls_headers['standard']
		ws.footer_str = self.xls_footers['standard']

		cell_style = xlwt.easyxf(_xs['xls_title'])
		c_specs = [
			('report_name', 1, 0, 'text', report_name),
		]

		row_data = self.xls_row_template(c_specs, ['report_name'])
		row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=cell_style)
		row_pos += 1

		c_specs = map(lambda x: self.render(x, self.col_specs_template, 'header', render_space={'_': _p._}), wanted_list)
		row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
		row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.rh_cell_style, set_column_size=True)
		ws.set_horz_split_pos(row_pos)

		# for line in objects:
		# 	c_specs = map(lambda x: self.render(x, self.col_specs_template, 'lines'), wanted_list)
		# 	row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
		# 	row_pos = self.xls_write_row(ws, row_pos, row_data, row_style=self.aml_cell_style)

case_list_xls('report.case_list.xls','court.case', parser=case_list_xls_parser)