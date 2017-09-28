import calendar
from datetime import datetime, timedelta, date
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
        if date:
            date_convert = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return (date_convert + timedelta(hours=7)).time()
        else:
            return None

    @staticmethod
    def convert_time(date):
        if date:
            date_convert = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return (date_convert + timedelta(hours=7)).time()
        else:
            return None

    @staticmethod
    def late_check(date):
        if date:
            time_limit = datetime.strptime('08:30', '%H:%M')
            date_convert = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            time_convert = (date_convert + timedelta(hours=7)).strftime('%H:%M')
            time_compare = datetime.strptime(time_convert, '%H:%M')
            if (time_limit - time_compare).total_seconds() < 0:
                return 1
            else:
                return None

        else:
            return None

    def _get_personal_absent(self, data):
        lines = []

        query = self.query_personal_absent(data)

        self.env.cr.execute(query)
        res = self.env.cr.dictfetchall()
        for r in res:
            if r['absent_out']:
                r['absent_out'] = self.convert_time_zone(r['absent_out'])
            if r['absent_in']:
                r['absent_in'] = self.convert_time_zone(r['absent_in'])
            lines.append(r)

        return lines

    def _get_absen(self, docs):
        hr_employee_attendance_pools = self.env['hr.employee.attendance']
        hr_employee_attendance_data = hr_employee_attendance_pools.search(['&', '&',
                                                                           ('employee_id.id', '=', docs.employee_id.id),
                                                                           ('name', '<=',
                                                                            str(docs.year_filter) + '-' +
                                                                            str(docs.month_filter) +
                                                                            '-' +
                                                                            str(calendar.monthrange(docs.year_filter,
                                                                                                    docs.month_filter)[
                                                                                    1])),
                                                                           ('name', '>=',
                                                                            str(docs.year_filter) + '-' +
                                                                            str(docs.month_filter) + '-1')
                                                                           ])
        return hr_employee_attendance_data

    @staticmethod
    def _date_different(from_date, to_date):
        if not from_date:
            return None
        if not to_date:
            return None
        return datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S') - datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')

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
            'periode': datetime.now().strftime("%B %Y"),
            'periode_year': datetime.now().strftime("%Y"),
            'employee_name': docs.employee_id.name,
            'employee_absen': self._get_personal_absent(docs),
            'employee_absen_data': self._get_absen(docs),
            'date_difference': self._date_different,
            'convert_time': self.convert_time,
            'late_check': self.late_check
        }
        return self.env['report'].render('prasetia_hr.report_personal_absen', docargs)
