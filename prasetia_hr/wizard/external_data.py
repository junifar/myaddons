import base64
from datetime import datetime

import pytz
from odoo.exceptions import ValidationError
from xlrd import XLRDError
from xlrd import open_workbook
from odoo import models, fields, api, _


class import_external_data(models.TransientModel):
    _name = 'external.import'

    name = fields.Char(string='Nama File', required=True)
    bin_file = fields.Binary(string="Upload File", required=True)
    finger_print_type = fields.Selection([(1, 'I. Format Lantai 2, 3, 4'), (2, 'II. Format Lantai 1')],
                                         string="Format Finger Print", required=True, default=1)

    @api.multi
    def _insert_sample(self, ctx):
        employee_attendance_pool = self.env['hr.employee.attendance']
        values = {
            'employee_id': 1,
            'name': ctx['attendance_name'],
            'absen_book_id': ctx['current_id']
        }
        employee_attendance_pool.create(values)
        return None

    @staticmethod
    def _check_str(value):
        try:
            value = str(int(value))
        except:
            pass
        return value

    def utcConvert(self, time_val):
        local = pytz.timezone(self.env.user.partner_id.tz)
        local_dt = local.localize(time_val, is_dst=None)
        return local_dt.astimezone(pytz.utc)

    def _update_check_date(self, ctx, noreg, date_absen, check_in, check_out):
        hr_employee_absen_book_pool = self.env['hr.employee.absen.book']
        hr_employee_absen_book_data = hr_employee_absen_book_pool.search([('id', '=', ctx['current_id'])])

        convert_date_absen = lambda x: x.strftime('%Y-%m-%d') if x is not None else None

        for data in hr_employee_absen_book_data:
            if data.name == convert_date_absen(date_absen):
                for line in data.absen_ids:
                    if line.employee_id.registration_id == noreg:
                        print noreg
                        print '===pass123==='
                        line.absent_in = self.utcConvert(check_in) if check_in is not None else None
                        line.absent_out = self.utcConvert(check_out) if check_out is not None else None
                        line.attendance_status = 'hadir'
        return None

    @staticmethod
    def _convert_month_to_int(month):
        months = dict(January=1,
                      February=2,
                      March=3,
                      April=4,
                      May=5,
                      June=6,
                      July=7,
                      August=8,
                      September=9,
                      October=10,
                      November=11,
                      December=12)
        return months[month]

    def _import_process_1(self, ctx):
        try:
            workbook = open_workbook(file_contents=base64.decodestring(self.bin_file))
            sheet = workbook.sheets()[0]
            if sheet.cell(3, 2).value is not None:
                cell_date_absen = sheet.cell(3, 2).value.split()
                year = int(cell_date_absen[3])
                month = self._convert_month_to_int(cell_date_absen[2])
                day = int(cell_date_absen[1])
                date_absen = datetime(year, month, day)
            else:
                date_absen = None

            for row in range(sheet.nrows):
                col_values = []
                if row >= 5:
                    if not sheet.cell(row, 6).value == '':
                        noreg = self._check_str(sheet.cell(row, 1).value)

                        value_hour = self._check_str(sheet.cell(row, 6).value)
                        value_minute = self._check_str(sheet.cell(row, 7).value)

                        try:
                            value_in = datetime.strptime(
                                '%s-%s-%s %s:%s' % (year, month, day, value_hour, value_minute),
                                '%Y-%m-%d %H:%M')
                        except TypeError:
                            value_in = None
                        except ValueError:
                            value_in = None

                        value_hour = self._check_str(sheet.cell(row, 8).value)
                        value_minute = self._check_str(sheet.cell(row, 9).value)
                        try:
                            value_out = datetime.strptime(
                                '%s-%s-%s %s:%s' % (year, month, day, value_hour, value_minute),
                                '%Y-%m-%d %H:%M')
                        except TypeError:
                            value_out = None
                        except ValueError:
                            value_out = None
                        col_values.append(value_out)

                        self._update_check_date(ctx, noreg, date_absen, value_in, value_out)
        except XLRDError:
            raise ValidationError(_('File Bukan Tipe Excel'))

    def _import_process_2(self, ctx):
        try:
            workbook = open_workbook(file_contents=base64.decodestring(self.bin_file))
            sheet = workbook.sheets()[0]

            for row in range(sheet.nrows):
                col_values = []
                if row >= 1:
                    if ctx['attendance_name'] == sheet.cell(row, 5).value:
                        noreg = self._check_str(sheet.cell(row, 2).value)
                        if noreg:
                            cell_date_absen = sheet.cell(row, 5).value.split("-")
                            year = int(cell_date_absen[0])
                            month = int(cell_date_absen[1])
                            day = int(cell_date_absen[2])
                            date_absen = datetime(year, month, day)

                            cell_time_in = sheet.cell(row, 9).value.split(":") if sheet.cell(row, 9).value else None
                            value_hour = int(cell_time_in[0]) if cell_time_in else None
                            value_minute = int(cell_time_in[1]) if cell_time_in else None
                            try:
                                value_in = datetime.strptime(
                                    '%d-%d-%d %d:%d' % (year, month, day, value_hour, value_minute),
                                    '%Y-%m-%d %H:%M')
                            except TypeError:
                                value_in = None
                            except ValueError:
                                value_in = None

                            cell_time_out = sheet.cell(row, 10).value.split(":") if sheet.cell(row, 10).value else None
                            value_hour = int(cell_time_out[1]) if cell_time_out else None
                            value_minute = int(cell_time_out[0]) if cell_time_out else None
                            try:
                                value_out = datetime.strptime(
                                    '%s-%s-%s %s:%s' % (year, month, day, value_hour, value_minute),
                                    '%Y-%m-%d %H:%M')
                            except TypeError:
                                value_out = None
                            except ValueError:
                                value_out = None
                            self._update_check_date(ctx, noreg, date_absen, value_in, value_out)
        except XLRDError:
            raise ValidationError(_('File Bukan Tipe Excel'))

    def _import_process(self, ctx):
        if self.finger_print_type == 1:
            self._import_process_1(ctx)
        else:
            self._import_process_2(ctx)

    @api.multi
    def show_data(self):
        ctx = self._context
        self._import_process(ctx)
        return None
