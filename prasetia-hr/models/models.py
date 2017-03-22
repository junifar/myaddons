# -*- coding: utf-8 -*-
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
            zk.connect()
        except Exception as e:
            raise exceptions.except_orm(_('Error'), _('Can\'t connect to device, IP : %s port %s : {}'.format(e) % (self.ip_address, self.port)))
        raise exceptions.except_orm(_('Success'), _('Connection Established'))
        return {}


class DeviceAttendanceImportUser(models.Model):
    _name = "device.attendance.user"

    device_attendance_id = fields.Many2one('device.attendance', required=True, string="Device Name")
    name = fields.Char(required=True, string='User Name')
    user_id = fields.Integer(string='User ID/UID')
