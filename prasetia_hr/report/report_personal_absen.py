from odoo import api, models


class ReportPersonalAbsen(models.AbstractModel):
    _name = 'report.prasetia_hr.report_personal_absen'

    @api.model
    def render_html(self, docids, data=None):
        # return None
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'employee_name': docs.employee_id.name
        }
        return self.env['report'].render('prasetia_hr.report_personal_absen', docargs)
