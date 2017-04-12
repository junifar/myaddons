from odoo import models, fields, api


class Employee(models.Model):
    _inherit = "hr.employee"

    registration_id = fields.Char(required=True, string='Noreg')
    birth_place = fields.Char(string='Birth Place')
    religion_id = fields.Many2one('hr.religion', string='Religion', required=False)
    street = fields.Char(string="Jalan")
    rt_rw = fields.Char(string="RT/RW")
    home_no = fields.Char(string="No. Rumah")
    kelurahan = fields.Char(string="Kelurahan")
    kecamatan = fields.Char(string="Kecamatan")
    kota = fields.Char(string="Kota")
    kode_pos = fields.Char(string="Kode Pos")
    street_ktp = fields.Char(string="Jalan")
    rt_rw_ktp = fields.Char(string="RT/RW")
    home_no_ktp = fields.Char(string="No. Rumah")
    kelurahan_ktp = fields.Char(string="Kelurahan")
    kecamatan_ktp = fields.Char(string="Kecamatan")
    kota_ktp = fields.Char(string="Kota")
    kode_pos_ktp = fields.Char(string="Kode Pos")
    name_relation = fields.Char(string="Nama")
    relation = fields.Char(string="Hubungan")
    street_emergency = fields.Char(string="Jalan")
    rt_rw_emergency = fields.Char(string="RT/RW")
    home_no_emergency = fields.Char(string="No. Rumah")
    kelurahan_emergency = fields.Char(string="Kelurahan")
    kecamatan_emergency = fields.Char(string="Kecamatan")
    kota_emergency = fields.Char(string="Kota")
    kode_pos_emergency = fields.Char(string="Kode Pos")
    phone_no_emergency = fields.Char(string="No. HP Darurat")
    license_ids = fields.One2many('hr.employee.driver.license', 'employee_id', string="List License")
    personal_account_ids = fields.One2many('hr.employee.personal.account', 'employee_id',
                                           string="List Personal Account")
    family_ids = fields.One2many('hr.employee.family', 'employee_id', string="List Employee Families")
    education_ids = fields.One2many('hr.employee.education', 'employee_id', string="List Employee Educations")
    work_history_ids = fields.One2many('hr.employee.work.history', 'employee_id', string="List Employee Work History")
    attendance_ids = fields.One2many('hr.employee.attendance', 'employee_id', string="List Employee Attendance")


class DriverLicense(models.Model):
    _name = "hr.employee.driver.license"

    employee_id = fields.Many2one('hr.employee', required=True)
    name = fields.Char(required=True, string='License ID')
    driver_license_type = fields.Many2one('hr.employee.driver.license.type', string='License Type', required=True)
    license_status = fields.Selection([(1, 'Active'), (2, 'Expired')])


class PersonalAccount(models.Model):
    _name = "hr.employee.personal.account"

    employee_id = fields.Many2one('hr.employee', required=True)
    personal_account_type_id = fields.Many2one('hr.employee.personal.account.type', string='Personal Account Type',
                                               required=True)
    name = fields.Char(required=True, string='Personal Account ID')
    registration_date = fields.Date(string='Registration Date')
    personal_account_status = fields.Selection([(1, 'Active'), (2, 'Expired')])


class PersonalAccountType(models.Model):
    _name = "hr.employee.personal.account.type"
    name = fields.Char(required=True, string='Personal Account Type')


class DriverLicenseType(models.Model):
    _name = "hr.employee.driver.license.type"
    name = fields.Char(required=True, string='Religion')


class Religion(models.Model):
    _name = "hr.religion"
    name = fields.Char(required=True, string='Religion')
