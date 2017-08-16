from odoo import models, fields, api


class Employee(models.Model):
    _inherit = "hr.employee"

    registration_id = fields.Char(required=True, string='Noreg')
    nama_panggilan = fields.Char(string='Nama Panggilan')
    birth_place = fields.Char(string='Birth Place')
    religion_id = fields.Many2one('hr.religion', string='Religion', required=False)
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('O', 'O'), ('AB', 'AB')], string="Golongan Darah")
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
    phone_no_emergency = fields.Char(string="Telepon Darurat")
    handphone_no_emergency = fields.Char(string="No. HP Darurat")
    license_ids = fields.One2many('hr.employee.driver.license', 'employee_id', string="List License")
    personal_account_ids = fields.One2many('hr.employee.personal.account', 'employee_id',
                                           string="List Personal Account")
    family_ids = fields.One2many('hr.employee.family', 'employee_id', string="List Employee Families")
    education_ids = fields.One2many('hr.employee.education', 'employee_id', string="List Employee Educations")
    work_history_ids = fields.One2many('hr.employee.work.history', 'employee_id', string="List Employee Work History")
    attendance_ids = fields.One2many('hr.employee.attendance', 'employee_id', string="List Employee Attendance")
    contract_ids = fields.One2many('hr.employee.contract', 'employee_id', string="List Employee Contract")
    date_join = fields.Date(string='Tanggal Masuk', required=True)
    mobile_phone_2 = fields.Char(string="Work Mobile 2")
    telepon = fields.Char(string="Telepon")
    telepon_ktp = fields.Char(string="Telepon KTP")

    directorate_id = fields.Many2one('hr.employee.directorate', string='Direktorat', required=True)

    no_npwp = fields.Char(string="No NPWP")
    tanggal_npwp = fields.Char(string="Tgl NPWP")

    no_bpjs_kesehatan = fields.Char(string="No BPJS Kesehatan")
    tanggal_kepesertaan_BPJS_kesehatan = fields.Char(string="Tgl Kepesertaan")

    no_bpjs_ketenagakerjaan = fields.Char(string="No BPJS Ketenagakerjaan")
    tanggal_kepesertaan_BPJS_ketenagakerjaan = fields.Char(string="Tgl Kepesertaan")

    @property
    def __str__(self):
        return self.registration_id + ' - ' + self.name


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
    name = fields.Char(required=True, string='Driver License Type')


class Religion(models.Model):
    _name = "hr.religion"
    name = fields.Char(required=True, string='Religion')


class Directorate(models.Model):
    _name = "hr.employee.directorate"
    company_id = fields.Many2one('res.company', required=True, string="Perusahaan")
    name = fields.Char(required=True, string='Religion')

    _sql_constraints = [
        ('unique_directorate_id', 'unique(company_id, name)', 'Data Already Exists')
    ]


class EmployeeStatusType(models.Model):
    _name = "hr.employee.status.type"
    name = fields.Char(required=True, string='Status Type')


class EmployeeContract(models.Model):
    _name = "hr.employee.contract"

    name = fields.Many2one('hr.employee.status.type', required=True, string='Status')
    employee_id = fields.Many2one('hr.employee', required=True)
    start_date = fields.Date(string='Mulai')
    end_date = fields.Date(string='Selesai')
    note = fields.Text(String="Note")


class KartuKeluarga(models.Model):
    _name = "hr.employee.kartu.keluarga"

    employee_id = fields.Many2one('hr.employee', required=True)
    name = fields.Char(string="Nomor KK", required=True)
    kepala_keluarga = fields.Char(string="Nama Kepala Keluarga", required=True)
    active = fields.Boolean(string='Active', default=False)
    kartu_keluarga_detail_ids = fields.One2many('hr.employee.kartu.keluarga.detail', 'kartu_keluarga_id',
                                                string="List Kartu Keluarga")


class KartuKeluargaDetail(models.Model):
    _name = "hr.employee.kartu.keluarga.detail"

    kartu_keluarga_id = fields.Many2one('hr.employee.kartu.keluarga', required=True)
    name = fields.Char(String="Nama Lengkap", required=True)
    relation = fields.Selection([('Kepala Keluarga', 'Kepala Keluarga'),
                                 ('Istri', 'Istri'), ('Anak', 'Anak'),
                                 ('Saudara', 'Saudara')], string="Hubungan Dalam Keluarga")
