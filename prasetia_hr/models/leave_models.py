from odoo import models, fields, api, exceptions, _


class LeavePeriode(models.Model):
    _name = "hr.employee.leave.periode"

    company_id = fields.Many2one('res.company', required=True, string="Perusahaan")
    name = fields.Char(string="Periode Cuti", required=True)
    leave_periode_detail_ids = fields.One2many('hr.employee.leave.periode.detail', 'leave_periode_id',
                                                 string="List Periode Detail Line")
    long_leave_periode_detail_ids = fields.One2many('hr.employee.long.leave.periode.detail', 'leave_periode_id',
                                               string="List Long Periode Detail Line")
    other_leave_periode_detail_ids = fields.One2many('hr.employee.other.leave.periode.detail', 'leave_periode_id',
                                               string="List Other Periode Detail Line")


class LeavePeriodeDetail(models.Model):
    _name = "hr.employee.leave.periode.detail"

    leave_periode_id = fields.Many2one('hr.employee.leave.periode', required=True, string="Periode Cuti")
    employee_id = fields.Many2one('hr.employee', required=True, string="Nama Pegawai")
    annual_leave = fields.Integer(string='Hak Cuti Tahunan', required=True)


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
