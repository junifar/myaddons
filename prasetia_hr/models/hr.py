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
    kartu_keluarga_ids = fields.One2many('hr.employee.kartu.keluarga', 'employee_id', string="List Employee KK")
    date_join = fields.Date(string='Tanggal Masuk', required=True)
    mobile_phone_2 = fields.Char(string="Work Mobile 2")
    telepon = fields.Char(string="Telepon")
    telepon_ktp = fields.Char(string="Telepon KTP")

    directorate_id = fields.Many2one('hr.employee.directorate', string='Direktorat', required=True)

    no_npwp = fields.Char(string="No NPWP")
    tanggal_npwp = fields.Date(string="Tgl NPWP")

    no_bpjs_kesehatan = fields.Char(string="No BPJS Kesehatan")
    tanggal_kepesertaan_BPJS_kesehatan = fields.Date(string="Tgl Kepesertaan")

    no_bpjs_ketenagakerjaan = fields.Char(string="No BPJS Ketenagakerjaan")
    tanggal_kepesertaan_BPJS_ketenagakerjaan = fields.Date(string="Tgl Kepesertaan")

    employee_bank_id = fields.Many2one('res.bank', string='Bank')
    employee_account_bank = fields.Char(string="Nomor Rekening")
    employee_account_bank_branch = fields.Char(string="Cabang")
    employee_status = fields.Char(string="Status Pekerja", compute="_compute_status_pekerja", store=True)
    show_bank_information = fields.Boolean(compute='_show_bank_information')

    def _show_bank_information(self):
        for data in self:
            data.show_bank_information = self.bankInformationState(data)

    def bankInformationState(self, data):
        val = False

        if data.resource_id.user_id == self.env.user:
            return True

        show_bank_information_pool = self.env['hr.employee.show.bank.information']
        show_bank_information_data = show_bank_information_pool.search([('name.id', '=', self.env.user.id)])

        if show_bank_information_data:
            return True

        return val

    def _compute_status_pekerja(self):
        for line in self.contract_ids:
            self.employee_status = line.name.name

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            values = '******'
            if record.registration_id:
                values = record.registration_id
            res.append((record.id, values + " - " + record.name))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('registration_id', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.onchange('user_id')
    def _onchange_user(self):
        self.work_email = self.work_email
        self.name = self.name
        self.image = self.image


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
                                 ('Saudara', 'Saudara'), ('Mertua', 'Mertua'),
                                 ('Keluarga Lain', 'Keluarga Lain')], string="Hubungan Dalam Keluarga")
    relation_position = fields.Integer(string='ke- ')
    status = fields.Selection([('hidup', 'Hidup'),
                               ('meninggal', 'Meninggal')], string="Keterangan Kondisi")


class CalendarYear(models.Model):
    _name = "hr.employee.calendar.year"

    name = fields.Char(String='Periode Tahun Berjalan', required=True)
    cuti_pemerintah_ids = fields.One2many('hr.employee.calendar.cuti.pemerintah', 'calendar_year_id',
                                          string='Cuti Bersama Pemerintah')
    libur_nasional_ids = fields.One2many('hr.employee.calendar.libur.nasional', 'calendar_year_id',
                                         string='Libur Nasional')


class CutiPemerintah(models.Model):
    _name = "hr.employee.calendar.cuti.pemerintah"

    calendar_year_id = fields.Many2one('hr.employee.calendar.year', required=True)
    tanggal_libur = fields.Date(string="Tanggal", required=True)
    description = fields.Char(string="Deskripsi")
    name = fields.Char(string="Tanggal Cuti Bersama Pemerintah", compute="_compute_desc_cuti_bersama_pemerintah",
                       store=True)
    _sql_constraints = [
        ('unique_cuti_pemerintah', 'unique(calendar_year_id, tanggal_libur)', 'Data Already Exists')
    ]

    @api.depends('tanggal_libur', 'description')
    def _compute_desc_cuti_bersama_pemerintah(self):
        for rec in self:
            rec.name = rec.tanggal_libur + " - " + rec.description


class LiburNasional(models.Model):
    _name = "hr.employee.calendar.libur.nasional"

    calendar_year_id = fields.Many2one('hr.employee.calendar.year', required=True)
    tanggal_libur = fields.Date(string="Tanggal", required=True)
    description = fields.Char(string="Deskripsi")
    name = fields.Char(string="Tanggal Libur Nasinal", compute="_compute_desc_libur_nasional",
                       store=True)

    @api.depends('tanggal_libur', 'description')
    def _compute_desc_libur_nasional(self):
        for rec in self:
            rec.name = rec.tanggal_libur + " - " + rec.description
