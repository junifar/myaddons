# -*- coding: utf-8 -*-
import json
from datetime import datetime

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

    device_attendance_id = fields.Many2one('device.attendance', required=True, string="Device Name", ondelete='cascade')
    name = fields.Char(required=True, string='User Name')
    user_id = fields.Integer(string='User ID/UID')
    employee_id = fields.Many2one('hr.employee', String="Employee Name", ondelete='cascade')

    _sql_constraints = [
        ('unique_device_attendance_id_employee_id', 'unique(device_attendance_id, employee_id)', 'Data Already Exists')
    ]


class AttendanceImport(models.Model):
    _name = "hr.employee.attendance.import"

    name = fields.Date(required=True, String="Date to Import")
    device_attendance_id = fields.Many2one('device.attendance', required=True, string="Device Name")
    attendance_import_line_ids = fields.One2many('hr.employee.attendance.import.line', 'attendance_import_id',
                                                 string="List Attendance Import Line")
    state = fields.Selection([('unprocessed', 'Unprocessed'), ('imported', 'Imported')], string="Status")

    def utcConvert(self, time_val):
        local = pytz.timezone(self.env.user.partner_id.tz)
        local_dt = local.localize(time_val, is_dst=None)
        return local_dt.astimezone(pytz.utc)

    @api.multi
    def action_unprocessed(self):
        self.state = 'unprocessed'

    @api.multi
    def action_imported(self):
        try:
            hr_employee_attendance = self.env['hr.employee.attendance']

            for attendances_import_line in self.attendance_import_line_ids:
                if attendances_import_line.name.employee_id.id:
                    values = {'name': self.name,
                              'employee_id': attendances_import_line.name.employee_id.id,
                              'absent_in': attendances_import_line.absent,
                              'absent_out': attendances_import_line.absent_out,
                              }
                    hr_employee_attendance.create(values)
            self.state = 'imported'
        except Exception as e:
            raise exceptions.except_orm(_('Error'), _(
                'Some of data on your record has been exists \n\n Error {}'.format(e)))

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
                            elif self.utcConvert(attendance.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z') \
                                    < data.absent:
                                data.absent = self.utcConvert(attendance.timestamp)
                            elif self.utcConvert(attendance.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z') \
                                    > data.absent_out:
                                data.absent_out = self.utcConvert(attendance.timestamp)
        except Exception as e:
            raise exceptions.except_orm(_('Error'), _(
                'Can\'t connect to device, IP : %s port %s : {}'.format(e) % (self.device_attendance_id.ip_address,
                                                                              self.device_attendance_id.port)))

        return {}


class AttendanceImportLine(models.Model):
    _name = "hr.employee.attendance.import.line"

    attendance_import_id = fields.Many2one('hr.employee.attendance.import', string="Attendance Import",
                                           ondelete='cascade')
    device_uid = fields.Integer(string="User ID in Device")
    name = fields.Many2one('device.attendance.user', required=True, string="Attendance User", ondelete='cascade')
    absent = fields.Datetime(String="Absent Date")
    absent_out = fields.Datetime(String="Absent Date")
    status = fields.Selection([(1, 'In'), (2, 'Out')], string="Status")


class Attendance(models.Model):
    _name = 'hr.employee.attendance'

    employee_id = fields.Many2one('hr.employee', string="Employee Name", ondelete='cascade', required=True)
    name = fields.Date(required=True, string="Date to Import")
    absent_in = fields.Datetime(string="Absent Date In")
    absent_out = fields.Datetime(string="Absent Date Out")
    note = fields.Text(string="Note")
    attendance_status = fields.Selection([('hadir', 'Present'),
                                          ('izin', 'Izin'), ('mangkir', 'Mangkir'),
                                          ('dinas', 'Dinas')],
                                         string="Status Kehadiran")
    leave_request_id = fields.Many2one('hr.employee.leave.request', string="Ijin Tidak Bekerja")
    absen_book_id = fields.Many2one('hr.employee.absen.book', string="Absen Book")
    terlambat = fields.Char(string='Terlambat')

    _sql_constraints = [
        ('unique_employee_id_absent_date', 'unique(employee_id, name)', 'Data Already Exists')
    ]

    @api.multi
    def post(self, values):
        self.create(values)
        print '===post called==='
        return None

    @api.multi
    def open_ui(self):
        ctx = self._context.copy()
        return {
            'name': _('Create Attendance'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.employee.attendance',
            'context': ctx,
        }


class AttendanceReport(models.Model):
    _name = 'hr.employee.attendance.report'

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_kanban_dashboard_datas())

    @api.one
    def _kanban_dashboard_graph(self):
        self.kanban_dashboard_graph = json.dumps(self.get_kanban_dashboard_graph_datas())

    name = fields.Char(required=True, string='Report Name')
    kanban_dashboard = fields.Text(compute='_kanban_dashboard')
    kanban_dashboard_graph = fields.Text(compute='_kanban_dashboard_graph')

    @api.multi
    def get_kanban_dashboard_datas(self):
        now = datetime.now()

        return {
            'title': 'Sum Data of Employee',
            'periode': now.strftime("%B - %Y"),
            'hadir': 200,
            'izin': 100,
            'absen': 50,
            'total_employee': 10,
        }

    @api.multi
    def get_kanban_dashboard_graph_datas(self):
        data = [{'label': _('Past'), 'y': 100.2, 'x': "12 Mar", 'name': '12 March 2017', 'type': 'past'},
                {'label': 'Coba', 'y': 200.2, 'x': "13 Mar", 'name': '13 March 2017', 'type': 'past'},
                {'label': 'Coba1', 'y': 500.2, 'x': "14 Mar", 'name': '14 March 2017', 'type': 'past'},
                {'label': 'Coba2', 'y': 10.2, 'x': "15 Mar", 'name': '15 March 2017', 'type': 'past'}]
        return [{'values': data}]


class leave_type(models.Model):
    _name = 'hr.employee.leave.request.type'

    name = fields.Char(String="Leave Type Name", required=True)


class leave_category(models.Model):
    _name = 'hr.employee.leave.request.category'

    name = fields.Char(String="Leave Type Name", required=True)


class leave_request(models.Model):
    _name = 'hr.employee.leave.request'

    serial_number = fields.Char(string='Form Number Number')
    tanggal_pengajuan = fields.Date(string='Tanggal Pengajuan', required=True)
    name = fields.Many2one('hr.employee', String="Employee Name", ondelete='cascade', required=True)
    department_id = fields.Many2one('hr.department', String="Departement", required=True)
    leave_category = fields.Selection([('cuti tahunan', 'Cuti Tahunan'), ('cuti panjang', 'Cuti Panjang'),
                                       ('other', 'Cuti Lainnya')], default='cuti tahunan')
    leave_type_id = fields.Many2one('hr.employee.leave.request.type', string="Leave Type")
    leave_category_ids = fields.Many2many('hr.employee.leave.request.category', 'rel_leave_request_category',
                                          string="Leave Category")
    # from_date = fields.Date(String="From Date", required=True)
    # to_date = fields.Date(String="To Date", required=True)
    reason = fields.Text(String="Reason", required=True)
    state = fields.Selection([('draft', 'Draft'), ('wait approval', 'Wait Approval HRD'), ('approved', 'Approved'),
                              ('cancel', 'Cancel'), ('reject', 'Reject')], string="Status")
    attachment = fields.Binary(String='Attachment')
    attachment_name = fields.Char(String='File Name')
    attendance_ids = fields.One2many('hr.employee.attendance', 'leave_request_id',
                                     string="List Izin Karyawan")
    leave_request_line = fields.One2many('hr.employee.leave.request.line', 'leave_request_id',
                                         string="List Izin Karyawan")
    leave_request_annual_leave_activity_line = fields.One2many('hr.employee.annual.leave.request.cuti',
                                                               'leave_request_id', string="Update Sisa Cuti")
    long_leave_request_annual_leave_activity_line = fields.One2many('hr.employee.annual.long.leave.request.cuti',
                                                                    'leave_request_id',
                                                                    string="Update Sisa Cuti 5 Tahunan")
    other_leave_request_annual_leave_activity_line = fields.One2many('hr.employee.other.leave.request.cuti',
                                                                     'leave_request_id',
                                                                     string="Update Sisa Cuti Lainnya")
    show_other_leave_type = fields.Boolean(compute='_show_other_leave_type')

    def _leave_type_state(self, data):
        val = False

        for check in data.leave_category_ids:
            if check.name == 'Cuti Lainnya':
                return True
        return val

    @api.depends('leave_category_ids.name')
    def _show_other_leave_type(self):
        for data in self:
            data.show_other_leave_type = self._leave_type_state(data)

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_wait_approval(self):
        self.state = 'wait approval'

    @api.multi
    def action_approved(self):
        self.state = 'approved'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'

    @api.multi
    def action_reject(self):
        self.state = 'reject'

    def get_annual_leave_used(self, id):
        hr_employee_annual_leave_request_cuti_pool = self.env['hr.employee.annual.leave.request.cuti']
        hr_employee_annual_leave_request_cuti_datas = hr_employee_annual_leave_request_cuti_pool.search([
            ('leave_periode_detail_id.id', '=', id)
        ])
        leave_remaining = 0
        if hr_employee_annual_leave_request_cuti_datas:
            for data in hr_employee_annual_leave_request_cuti_datas:
                if data.leave_request_id.state == 'approved':
                    leave_remaining += data.annual_leave_used
        return leave_remaining

    @api.multi
    def sync_leave(self):
        annual_leave_employee_pool = self.env['hr.employee.leave.periode.detail']
        annual_leave_employee_datas = annual_leave_employee_pool.search(
            ['&', '&', ('employee_id.id', '=', self.name.id),
             ('start_periode', '<=', datetime.now().strftime("%Y-%m-%d")),
             ('end_periode', '>=', datetime.now().strftime("%Y-%m-%d"))
             ])
        if annual_leave_employee_datas:
            for data in annual_leave_employee_datas:
                is_found = False
                for check in self.leave_request_annual_leave_activity_line:
                    if check.leave_periode_detail_id.id == data.id:
                        is_found = True
                        break
                if not is_found:
                    values = {
                        'leave_request_id': self.id,
                        'leave_periode_detail_id': data.id,
                        'annual_leave': data.annual_leave,
                        'start_periode': data.start_periode,
                        'end_periode': data.end_periode,
                        # 'annual_leave_remaining': data.annual_leave_used
                        'annual_leave_remaining': data.annual_leave - self.get_annual_leave_used(data.id)
                    }
                    self.leave_request_annual_leave_activity_line.create(values)
        return None

    @api.multi
    def import_data(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'external.import',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }

    @api.multi
    def sync_long_leave(self):
        long_leave_employee_pool = self.env['hr.employee.long.leave.periode.detail']
        long_leave_employee_data = long_leave_employee_pool.search([
            '&', '&', ('employee_id.id', '=', self.name.id),
            ('start_periode', '<=', datetime.now().strftime("%Y-%m-%d")),
            ('end_periode', '>=', datetime.now().strftime("%Y-%m-%d"))
        ])
        if long_leave_employee_data:
            for data in long_leave_employee_data:
                is_found = False
                for check in self.long_leave_request_annual_leave_activity_line:
                    if check.leave_periode_detail_id.id == data.id:
                        is_found = True
                        break
                if not is_found:
                    values = {
                        'leave_request_id': self.id,
                        'long_leave_periode_detail_id': data.id,
                        'annual_leave': data.annual_leave,
                        'start_periode': data.start_periode,
                        'end_periode': data.end_periode,
                        'annual_leave_remaining': data.annual_leave_used
                    }
                    self.long_leave_request_annual_leave_activity_line.create(values)
        return None

    @api.multi
    def sync_Other_leave(self):
        other_leave_employee_pool = self.env['hr.employee.other.leave.periode.detail']
        other_leave_employee_data = other_leave_employee_pool.search([
            '&', '&', ('employee_id.id', '=', self.name.id),
            ('start_periode', '<=', datetime.now().strftime("%Y-%m-%d")),
            ('end_periode', '>=', datetime.now().strftime("%Y-%m-%d"))
        ])
        if other_leave_employee_data:
            for data in other_leave_employee_data:
                is_found = False
                for check in self.other_leave_request_annual_leave_activity_line:
                    if check.leave_periode_detail_id.id == data.id:
                        is_found = True
                        break
                if not is_found:
                    values = {
                        'leave_request_id': self.id,
                        'other_leave_periode_detail_id': data.id,
                        'other_leave': data.other_leave,
                        'start_periode': data.start_periode,
                        'end_periode': data.end_periode,
                        'other_leave_remaining': data.other_leave_used
                    }
                    self.other_leave_request_annual_leave_activity_line.create(values)
        return None


class leave_request_line(models.Model):
    _name = 'hr.employee.leave.request.line'

    name = fields.Date(required=True, string="Date to Import")
    leave_request_id = fields.Many2one('hr.employee.leave.request', string="Ijin Tidak Bekerja")
    note = fields.Text(string="Keterangan")

    _sql_constraints = [
        ('unique_employee_request_line', 'unique(leave_request_id, name)', 'Data Already Exists')
    ]


class leave_request_annual_leave_activity(models.Model):
    _name = 'hr.employee.annual.leave.request.cuti'

    leave_request_id = fields.Many2one('hr.employee.leave.request', string="Ijin Tidak Bekerja")
    leave_periode_detail_id = fields.Many2one('hr.employee.leave.periode.detail', required=True,
                                              string="Periode Cuti Line")
    annual_leave = fields.Integer(string='Hak Cuti Tahunan', required=True)
    start_periode = fields.Date(string='Tanggal Mulai Berlaku', required=True)
    end_periode = fields.Date(string='Tanggal Akhir Berlaku', required=True)
    annual_leave_remaining = fields.Integer(string='Sisa Cuti Tahunan', requird=True)
    annual_leave_used = fields.Integer(string='Cuti Terpakai')


class leave_request_long_leave_activity(models.Model):
    _name = 'hr.employee.annual.long.leave.request.cuti'

    leave_request_id = fields.Many2one('hr.employee.leave.request', string="Ijin Tidak Bekerja")
    long_leave_periode_detail_id = fields.Many2one('hr.employee.long.leave.periode.detail', required=True,
                                                   string="Periode Cuti Lima Tahunan Line")
    annual_leave = fields.Integer(string='Hak Cuti 5 Tahunan', required=True)
    start_periode = fields.Date(string='Tanggal Mulai Berlaku', required=True)
    end_periode = fields.Date(string='Tanggal Akhir Berlaku', required=True)
    annual_leave_remaining = fields.Integer(string='Sisa Hak Cuti 5 Tahunan', required=True)
    annual_leave_used = fields.Integer(string='Cuti Terpakai')


class leave_request_other_activity(models.Model):
    _name = 'hr.employee.other.leave.request.cuti'

    leave_request_id = fields.Many2one('hr.employee.leave.request', string="Ijin Tidak Bekerja")
    other_leave_periode_detail_id = fields.Many2one('hr.employee.other.leave.periode.detail', required=True,
                                                    string="Periode Cuti Lainnya Line")
    other_leave = fields.Integer(string='Hak Cuti 5 Tahunan', required=True)
    start_periode = fields.Date(string='Tanggal Mulai Berlaku', required=True)
    end_periode = fields.Date(string='Tanggal Akhir Berlaku', required=True)
    other_leave_remaining = fields.Integer(string='Sisa Hak Cuti Lainnya', required=True)
    other_leave_used = fields.Integer(string='Cuti Terpakai')


class show_bank_information(models.Model):
    _name = 'hr.employee.show.bank.information'

    name = fields.Many2one('res.users', required=True)
