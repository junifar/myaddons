from odoo import models, fields, api, exceptions, _


class LeavePeriode(models.Model):
    _name = "hr.employee.leave.periode"

    company_id = fields.Many2one('res.company', required=True, string="Perusahaan")
    name = fields.Char(string="Periode Cuti", required=True)
    default_annual_leave = fields.Integer(String="Standar Cuti (Hari)", required=True)
    leave_periode_detail_ids = fields.One2many('hr.employee.leave.periode.detail', 'leave_periode_id',
                                               string="List Periode Detail Line")
    long_leave_periode_detail_ids = fields.One2many('hr.employee.long.leave.periode.detail', 'leave_periode_id',
                                                    string="List Long Periode Detail Line")
    other_leave_periode_detail_ids = fields.One2many('hr.employee.other.leave.periode.detail', 'leave_periode_id',
                                                     string="List Other Periode Detail Line")

    @api.multi
    def action_import_employee(self):
        hr_employee_leave_periode_detail = self.env['hr.employee.leave.periode.detail']

        hr_employee_datas = self.env['hr.employee'].search([('resource_id.active', '=', True)])
        if hr_employee_datas:
            for data in hr_employee_datas:
                # print data.name_related.encode("utf-8")

                is_found = False
                for check in hr_employee_leave_periode_detail.search([('leave_periode_id', '=', self.id)]):
                    if check.employee_id.id == data.id:
                        is_found = True
                        break

                if not is_found:
                    values = {
                        'leave_periode_id': self.id,
                        'employee_id': data.id,
                        'annual_leave': self.default_annual_leave
                    }
                    hr_employee_leave_periode_detail.create(values)

        return None


class LeavePeriodeDetail(models.Model):
    _name = "hr.employee.leave.periode.detail"

    leave_periode_id = fields.Many2one('hr.employee.leave.periode', required=True, string="Periode Cuti")
    employee_id = fields.Many2one('hr.employee', required=True, string="Nama Pegawai")
    annual_leave = fields.Integer(string='Hak Cuti Tahunan', required=True)

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
