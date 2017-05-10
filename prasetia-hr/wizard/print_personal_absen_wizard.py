from datetime import datetime
from odoo import models, fields, api


class personal_absen_report(models.TransientModel):
    _name = 'personal.absent.report'
    _description = 'Personal absent report'

    employee_id = fields.Many2one('hr.employee', required=True)
    month_filter = fields.Selection(selection=[
        (1, 'Januari'),
        (2, 'Februari'),
        (3, 'Maret'),
        (4, 'April'),
        (5, 'Mei'),
        (6, 'Juni'),
        (7, 'Juli'),
        (8, 'Agustus'),
        (9, 'September'),
        (10, 'Oktober'),
        (11, 'November'),
        (12, 'Desember')
    ], string="Bulan")
    year_filter = fields.Integer(string="Tahun", default=datetime.now().year)

    @api.multi
    def show_data(self):
        print '===works==='
        return None