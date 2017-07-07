from datetime import datetime, timedelta
import pytz
from odoo import api, models


class ReportPersonalAbsen(models.AbstractModel):
    _name = 'report.prasetia_hr.report_personal_absen'

    @staticmethod
    def query_personal_absent(data):
        query = """
                SELECT
                    "public".hr_employee_attendance."id",
                    "public".hr_employee_attendance.create_uid,
                    "public".hr_employee_attendance.absent_in,
                    "public".hr_employee_attendance.employee_id,
                    "public".hr_employee_attendance."name",
                    "public".hr_employee_attendance.absent_out,
                    "public".hr_employee_attendance.write_uid,
                    "public".hr_employee_attendance.note,
                    "public".hr_employee_attendance.write_date,
                    "public".hr_employee_attendance.create_date,
                    "public".hr_employee_attendance.absent_out::TIME - "public".hr_employee_attendance.absent_in::TIME
                      AS work_hours
                    FROM
                    "public".hr_employee_attendance
                    WHERE
                        EXTRACT(MONTH FROM "public".hr_employee_attendance."name") = %s AND
                        EXTRACT(YEAR FROM "public".hr_employee_attendance."name") = %s AND
                        "public".hr_employee_attendance.employee_id = %d
        """ % (data.month_filter, data.year_filter, data.employee_id.id)
        return query

    @staticmethod
    def convert_time_zone(date):
        date_convert = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return (date_convert + timedelta(hours=7)).time()

    def _get_personal_absent(self, data):
        lines = []

        query = self.query_personal_absent(data)

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            r['absent_out'] = self.convert_time_zone(r['absent_out'])
            r['absent_in'] = self.convert_time_zone(r['absent_in'])
            lines.append(r)

        return lines

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
            'employee_name': docs.employee_id.name,
            'employee_absen': self._get_personal_absent(docs)
        }
        return self.env['report'].render('prasetia_hr.report_personal_absen', docargs)
