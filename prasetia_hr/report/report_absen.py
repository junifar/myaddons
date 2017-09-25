import pdb

from datetime import datetime, timedelta
import pytz
from odoo import api, models


class ReportAbsen(models.AbstractModel):
    _name = 'report.prasetia_hr.report_absen'

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
                        "public".hr_employee_attendance."name" = '%s'
        """ % (data.company_id.id, data.date_filter if data.date_filter else '01-01-2017')
        return query

    @staticmethod
    def query_custom_absent(data):
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
                            "public".hr_employee_attendance."name" >= '%s' AND
                            "public".hr_employee_attendance."name" <= '%s'
            """ % (data.company_id.id, data.date_filter_from if data.date_filter_from else '01-01-2017',
                   data.date_filter_to if data.date_filter_to else '01-01-2017')
        return query

    @staticmethod
    def query_bulanan_absent(data):
        query = """
            SELECT
            "public".hr_employee.id,
            "public".hr_employee.registration_id,
            "public".resource_resource."name",
            "public".hr_employee_attendance.attendance_status,
            Count("public".hr_employee_attendance."id") AS total
            FROM
            "public".hr_employee
            LEFT JOIN "public".hr_employee_attendance ON "public".hr_employee_attendance.employee_id = "public".hr_employee."id"
            LEFT JOIN "public".resource_resource ON "public".hr_employee.resource_id = "public".resource_resource."id"
            WHERE
            "public".resource_resource.company_id = %d AND
            EXTRACT(MONTH FROM "public".hr_employee_attendance."name") = %d AND
            EXTRACT(YEAR FROM "public".hr_employee_attendance."name") = %d
            GROUP BY
            "public".hr_employee."id",
            "public".hr_employee.registration_id,
            "public".resource_resource."name",
            "public".hr_employee_attendance.attendance_status,
            "public".hr_employee.name_relation
        """ % (data.company_id.id, data.month_filter, data.year_filter)
        return query

    @staticmethod
    def query_employee_list(data):
        query = """
            SELECT
            "public".hr_employee.id,
            "public".hr_employee.registration_id,
            "public".resource_resource."name"
            FROM
            "public".hr_employee
            LEFT JOIN "public".resource_resource ON "public".hr_employee.resource_id = "public".resource_resource."id"
            WHERE
            "public".resource_resource.company_id = '%d' AND
            "public".resource_resource.active = 't'
            ORDER BY
            "public".resource_resource."name" ASC
        """ % data.company_id.id
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

    def _get_custom_absent(self, data):
        lines = []
        query = self.query_custom_absent(data)

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            if r['absent_out']:
                r['absent_out'] = self.convert_time_zone(r['absent_out'])
            if r['absent_in']:
                r['absent_in'] = self.convert_time_zone(r['absent_in'])
            lines.append(r)

        return lines

    def _get_employee_list(self, data):
        lines = []
        query = self.query_employee_list(data)

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            lines.append(r)

        return lines

    def _get_bulanan_absent(self, data):
        lines = []
        query = self.query_bulanan_absent(data)

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            lines.append(r)

        return lines

    def _process_report(self, data):
        if data.report_type == 'Harian':
            self._get_harian_absent(data)

        if data.report_type == 'Bulanan':
            self._get_bulanan_absent(data)

    @api.model
    def render_html(self, docids, data=None):

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        process_report = {
            'Harian': self._get_harian_absent(docs),
            'Bulanan': self._get_bulanan_absent(docs),
            'Custom': self._get_custom_absent(docs)
        }

        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'report_type': docs.report_type,
            'data_absen': process_report[docs.report_type],
            'employee_name': self._get_employee_list(docs)
            # 'data_absen': self._process_report(docs)
        }

        return self.env['report'].render('prasetia_hr.report_absen', docargs)
