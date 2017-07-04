from odoo import api, models


class ReportAbsen(models.AbstractModel):
    _name = 'report.report_absen'

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'report_type': data.get('form').get('report_type'),
            'date_filter': data.get('form').get('date_filter'),
            'bulan_filter': data.get('form').get('month_filter'),
            'tahun_filter': data.get('form').get('year_filter'),
            'transactions': self._get_atk_list(data.get('form'))
        }

        return self.env['report'].render('prasetia-hr.report_absen', docargs)
