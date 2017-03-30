# -*- coding: utf-8 -*-
import pytz
from odoo import models, fields, api, exceptions, _
from zk import ZK


class EmployeeFamily(models.Model):
    _name = "hr.employee.family"

    employee_id = fields.Many2one('hr.employee', required=True)
    name = fields.Char(required=True, string='Nama')
    birth_place = fields.Char(string='Tempat Lahir')
    date_birth = fields.Date(string="Tanggal Lahir")
    relation_status = fields.Char(string="Hubungan Keluarga")


class EmployeeEducation(models.Model):
    _name = "hr.employee.education"

    employee_id = fields.Many2one('hr.employee', required=True)
    name = fields.Char(required=True, string='Nama Sekolah')
    major = fields.Char(string='Jurusan')
    city = fields.Char(string='Kota')
    year_start = fields.Char(string='Tahun Mulai')
    year_finish = fields.Char(string='Tahun Selesai')
    graduated = fields.Selection([(1, 'Lulus'), (2, 'Tidak Lulus')])
    remark = fields.Text(string='Keterangan')


class WorkHistory(models.Model):
    _name = "hr.employee.work.history"

    employee_id = fields.Many2one('hr.employee', required=True)
    name = fields.Char(required=True, string='Nama Perusahaan')
    role = fields.Char(string='Jabatan')
    city = fields.Char(string='Kota')
    year_start = fields.Char(string='Tahun Mulai')
    year_end = fields.Char(string='Tahun Selesai')
    reason_leave = fields.Text(string='Alasan Resign')
    note = fields.Text(string='Keterangan')


class DeviceAttendanceType(models.Model):
    _name = "device.attendance.type"

    name = fields.Char(required=True, string='Device Type Name')


class DeviceAttendance(models.Model):
    _name = "device.attendance"

    name = fields.Char(required=True, string='Device Name')
    device_attendance_type_id = fields.Many2one('device.attendance.type', string='Device Type')
    ip_address = fields.Char(string='IP Address')
    port = fields.Char(string="Port")
    device_attendance_user_ids = fields.One2many('device.attendance.user', 'device_attendance_id',
                                                 string="List User In Fingerprint Device")

    @api.multi
    def import_user(self):
        zk = ZK(self.ip_address, port=int(self.port), timeout=5)
        try:
            conn = zk.connect()
            users = conn.get_users()
            for user in users:
                self.device_attendance_user_ids = [{'name': user.name, 'user_id': user.uid}]
        except Exception as e:
            raise exceptions.except_orm(_('Error'), _(
                'Can\'t connect to device, IP : %s port %s : {}'.format(e) % (self.ip_address, self.port)))
        return {}


class DeviceAttendanceImportUser(models.Model):
    _name = "device.attendance.user"

    device_attendance_id = fields.Many2one('device.attendance', required=True, string="Device Name")
    name = fields.Char(required=True, string='User Name')
    user_id = fields.Integer(string='User ID/UID')
    employee_id = fields.Many2one('hr.employee', String="Employee Name")


class AttendanceImport(models.Model):
    _name = "hr.employee.attendance.import"

    name = fields.Date(required=True, String="Date to Import")
    device_attendance_id = fields.Many2one('device.attendance', required=True, string="Device Name")
    attendance_import_line_ids = fields.One2many('hr.employee.attendance.import.line', 'attendance_import_id',
                                                 string="List Attendance Import Line")

    def utcConvert(self, time_val):
        local = pytz.timezone(self.env.user.partner_id.tz)
        local_dt = local.localize(time_val, is_dst=None)
        return local_dt.astimezone(pytz.utc)

    @api.multi
    def import_absent(self):
        device_attendance_users = self.env['device.attendance.user']. \
            search([('device_attendance_id', '=', self.device_attendance_id.id)])

        zk = ZK(self.device_attendance_id.ip_address, port=int(self.device_attendance_id.port), timeout=5)
        try:
            conn = zk.connect()

            attendances = conn.get_attendance()
            for attendance in attendances:
                if str(attendance.timestamp.date()) == str(self.name):
                    val = None
                    for device_attendance_user in device_attendance_users:
                        if str(attendance.user_id) == str(device_attendance_user.user_id):
                            val = device_attendance_user.id
                            break
                    if val is not None:
                        count = self.env['hr.employee.attendance.import.line'].search_count(
                            [('attendance_import_id', '=', self.id),
                             ('device_uid', '=', attendance.user_id)])
                        if count == 0:
                            self.attendance_import_line_ids = [{'name': val,
                                                                'attendance_import_id': self.id,
                                                                'absent': self.utcConvert(attendance.timestamp),
                                                                'device_uid': attendance.user_id}]
                        else:
                            data = self.env['hr.employee.attendance.import.line'].search(
                                [('attendance_import_id', '=', self.id), ('device_uid', '=', attendance.user_id)])
                            # data.absent_out = self.utcConvert(attendance.timestamp)
                            if data.absent_out is None:
                                data.absent_out = self.utcConvert(attendance.timestamp)
                            elif self.utcConvert(attendance.timestamp) < data.absent:
                                data.absent = self.utcConvert(attendance.timestamp)
                            elif self.utcConvert(attendance.timestamp) > data.absent_out:
                                data.absent_out = self.utcConvert(attendance.timestamp)
                                # if self.attendance_import_line_ids:
                                #     for line in self.attendance_import_line_ids:
                                #         print line.device_uid
                                #         if line.device_uid == attendance.user_id:
                                #             if line.absent_out is None:
                                #                 line.absent_out = self.utcConvert(attendance.timestamp)
                                #                 break
                                #             elif self.utcConvert(attendance.timestamp) < line.absent:
                                #                 line.absent = self.utcConvert(attendance.timestamp)
                                #                 break
                                #             elif self.utcConvert(attendance.timestamp) > line.absent_out:
                                #                 line.absent_out = self.utcConvert(attendance.timestamp)
                                #                 break
                                #         else:
                                #             self.attendance_import_line_ids = [{'name': val,
                                #                                                 'attendance_import_id': self.id,
                                #                                                 'absent': self.utcConvert(attendance.timestamp),
                                #                                                 'device_uid': attendance.user_id}]
                                # else:
                                #     self.attendance_import_line_ids = [{'name': val,
                                #                                         'attendance_import_id': self.id,
                                #                                         'absent': self.utcConvert(attendance.timestamp),
                                #                                         'device_uid': attendance.user_id}]
        except Exception as e:
            raise exceptions.except_orm(_('Error'), _(
                'Can\'t connect to device, IP : %s port %s : {}'.format(e) % (self.device_attendance_id.ip_address,
                                                                              self.device_attendance_id.port)))

        return {}


class AttendanceImportLine(models.Model):
    _name = "hr.employee.attendance.import.line"

    attendance_import_id = fields.Many2one('hr.employee.attendance.import', string="Attendance Import")
    device_uid = fields.Integer(string="User ID in Device")
    name = fields.Many2one('device.attendance.user', required=True, string="Attendance User")
    absent = fields.Datetime(String="Absent Date")
    absent_out = fields.Datetime(String="Absent Date")
    status = fields.Selection([(1, 'In'), (2, 'Out')], string="Status")
