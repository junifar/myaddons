from odoo import api, models


class ReportPersonalAbsen(models.AbstractModel):
    _name = 'report.personal_absen'

    @api.multi
    def render_html(self, data):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
        }
        return self.env['report'].render('prasetia-hr.report_personal_absen', docargs)
