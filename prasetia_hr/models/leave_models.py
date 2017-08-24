from datetime import datetime

from odoo import models, fields, api, exceptions, _


class LeavePeriode(models.Model):
    _name = "hr.employee.leave.periode"

    company_id = fields.Many2one('res.company', required=True, string="Perusahaan")
    name = fields.Char(string="Periode Cuti", required=True)
    default_annual_leave = fields.Integer(string="Standar Cuti (Hari)", required=True)
    # government_holiday = fields.Integer(string="C.B Pemerintah", required=True, default=0)
    # company_holiday = fields.Integer(string="C.B Perusahaan", required=True, default=0)
    leave_periode_detail_ids = fields.One2many('hr.employee.leave.periode.detail', 'leave_periode_id',
                                               string="List Periode Detail Line")
    long_leave_periode_detail_ids = fields.One2many('hr.employee.long.leave.periode.detail', 'leave_periode_id',
                                                    string="List Long Periode Detail Line")
    other_leave_periode_detail_ids = fields.One2many('hr.employee.other.leave.periode.detail', 'leave_periode_id',
                                                     string="List Other Periode Detail Line")
    cuti_pemerintah_ids = fields.Many2many('hr.employee.calendar.cuti.pemerintah', 'rel_cuti_pemerintah_leave_periode',
                                           string="Cuti Bersama Pemerintah")
    cuti_perusahaan_ids = fields.One2many('hr.employee.calendar.cuti.perusahaan', 'leave_periode_id',
                                                     string="List Cuti Perusahaan Detail Line")

    @api.multi
    def action_import_employee(self):
        hr_employee_leave_periode_detail = self.env['hr.employee.leave.periode.detail']

        hr_employee_datas = self.env['hr.employee'].search(['&', ('resource_id.active', '=', True),
                                                            ('date_join', '!=', False)])
        if hr_employee_datas:
            for data in hr_employee_datas:
                # print data.name_related.encode("utf-8")

                is_found = False
                for check in hr_employee_leave_periode_detail.search([('leave_periode_id', '=', self.id)]):
                    if check.employee_id.id == data.id:
                        is_found = True
                        break

                join_date = datetime.strptime(data.date_join, "%Y-%m-%d").date()

                if not is_found:
                    values = {
                        'leave_periode_id': self.id,
                        'employee_id': data.id,
                        'annual_leave': self.default_annual_leave,
                        'start_periode': datetime.strptime('01-01-' + self.name, "%d-%m-%Y").date(),
                        'end_periode': datetime.strptime('30-06-' + str(int(self.name) + 1), "%d-%m-%Y").date()
                    }
                    hr_employee_leave_periode_detail.create(values)

        return None


class LeavePeriodeDetail(models.Model):
    _name = "hr.employee.leave.periode.detail"

    leave_periode_id = fields.Many2one('hr.employee.leave.periode', required=True, string="Periode Cuti")
    employee_id = fields.Many2one('hr.employee', required=True, string="Nama Pegawai")
    annual_leave = fields.Integer(string='Hak Cuti Tahunan', required=True)
    annual_leave_used = fields.Integer(string='Cuti Terpakai', requird=True)
    start_periode = fields.Date(string='Tanggal Mulai Berlaku', required=True)
    end_periode = fields.Date(string='Tanggal Akhir Berlaku', required=True)
    locked = fields.Boolean(string='Locked', default=False)

    _sql_constraints = [
        ('unique_leave_periode_id_employee_id', 'unique(leave_periode_id, employee_id)', 'Employee Already Registered')
    ]


class LongLeavePeriodeDetail(models.Model):
    _name = "hr.employee.long.leave.periode.detail"

    leave_periode_id = fields.Many2one('hr.employee.leave.periode', required=True, string="Periode Cuti")
    employee_id = fields.Many2one('hr.employee', required=True, string="Nama Pegawai")
    annual_leave = fields.Integer(string='Hak Cuti 5 Tahunan', required=True)


class LeaveType(models.Model):
    _name = "hr.employee.leave.type"
    name = fields.Char(required=True, string='Type Cuti')


class OtherLeavePeriodeDetail(models.Model):
    _name = "hr.employee.other.leave.periode.detail"

    leave_periode_id = fields.Many2one('hr.employee.leave.periode', required=True, string="Periode Cuti")
    leave_type_id = fields.Many2one('hr.employee.leave.type', requred=True, string="Jenis Cuti")
    employee_id = fields.Many2one('hr.employee', required=True, string="Nama Pegawai")
    annual_leave = fields.Integer(string='Hak Cuti Lainnya', required=True)


class CutiPerusahaan(models.Model):
    _name = "hr.employee.calendar.cuti.perusahaan"

    leave_periode_id = fields.Many2one('hr.employee.leave.periode', required=True, string="Periode Cuti")
    tanggal_libur = fields.Date(string="Tanggal", required=True)
    description = fields.Char(string="Deskripsi")
    _sql_constraints = [
        ('unique_cuti_perusahaan', 'unique(leave_periode_id, tanggal_libur)', 'Data Already Exists')
    ]
