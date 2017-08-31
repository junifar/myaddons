import pdb

from datetime import datetime, timedelta
import pytz
from odoo import api, models


class ReportPersonalLeave(models.AbstractModel):
    _name = 'report.prasetia_hr.report_personal_leave'

    @staticmethod
    def query_harian_absent(data):
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
                      AS work_hours,
                    "public".hr_employee.name_related,
                    "public".hr_employee.registration_id,
                    "public".res_company."name" AS company_name
                    FROM
                    "public".hr_employee_attendance
                    LEFT JOIN "public".hr_employee ON "public".hr_employee_attendance.employee_id = "public".hr_employee."id"
                    LEFT JOIN "public".resource_resource ON "public".hr_employee.resource_id = "public".resource_resource."id"
                    LEFT JOIN "public".res_company ON "public".resource_resource.company_id = "public".res_company."id"
                    WHERE
                        "public".resource_resource.company_id = %d AND
                        "public".hr_employee_attendance.employee_id = '%s'
        """ % (data.company_id.id, data.employee_id.id)
        return query

    @staticmethod
    def convert_time_zone(date):
        date_convert = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return (date_convert + timedelta(hours=7)).time()

    def _get_harian_absent(self, data):
        lines = []
        query = self.query_harian_absent(data)

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            if r['absent_out']:
                r['absent_out'] = self.convert_time_zone(r['absent_out'])
            if r['absent_in']:
                r['absent_in'] = self.convert_time_zone(r['absent_in'])
            lines.append(r)

        return lines

    def _get_leave_data(self, docs):
        leave_periode_detail_pools = self.env['hr.employee.leave.periode.detail']
        leave_periode_detail_data = leave_periode_detail_pools.search(['&', '&',
                                                                       ('employee_id.id', '=', docs.employee_id.id),
                                                                       ('start_periode', '<=',
                                                                        datetime.now().strftime("%Y-%m-%d")),
                                                                       ('end_periode', '>=',
                                                                        datetime.now().strftime("%Y-%m-%d"))
                                                                       ])
        return leave_periode_detail_data

    def _get_government_leave_data(self, docs):
        leave_periode_pools = self.env['hr.employee.leave.periode']
        leave_periode_data = leave_periode_pools.search([('name', '=', datetime.now().strftime("%Y"))])
        count_data = 0
        for data in leave_periode_data:
            for child in data.cuti_pemerintah_ids:
                count_data += 1

        return count_data

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        process_report = {
            'Harian': None,
            'Bulanan': None,
            'Custom': None
        }

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'employee_name': docs.employee_id.name,
            'data_absen': None,
            'periode': datetime.now().strftime("%B %Y"),
            'leave_data': self._get_leave_data(docs),
            'gov_leave_data': self._get_government_leave_data(docs)
        }

        # 'data_absen': process_report[docs.report_type]

        return self.env['report'].render('prasetia_hr.report_personal_leave', docargs)
