import pdb

from openerp import api, models


class ReportFamily(models.AbstractModel):
    _name = 'report.prasetia_hr.family_report'

    def _get_family_list(self, data):
        lines = []

        query = """
                    SELECT
                    "public".hr_employee_family."name",
                    "public".hr_employee_family.birth_place,
                    "public".hr_employee_family.relation_status
                    FROM
                    "public".hr_employee_family
                """
        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            lines.append(r)
        return lines

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        family_list = self._get_family_list(docs)

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'family_list': family_list,
            'date_filter': docs.date_filter,
            'transactions': self._get_family_list(docs)
        }

        return self.env['report'].render('prasetia_hr.family_report', docargs)
