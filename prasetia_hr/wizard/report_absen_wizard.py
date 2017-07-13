from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError

class report_absen_wizard(models.TransientModel):
    _name = 'hr.employee.report.absent.wizard'
    _description = 'Report Absent Priodicaly'

    company_id = fields.Many2one('res.company', required=True)
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
    ], string="Bulan", required=True)
    year_filter = fields.Integer(string="Tahun", default=datetime.now().year, required=True)

    @api.multi
    def show_data(self):
        return None
