from odoo import api, models


class ReportOrganizationStructure(models.AbstractModel):
    _name = 'report.prasetia_hr.report_organization_structure'

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs
        }

        return self.env['report'].render('prasetia_hr.report_organization_structure', docargs)
