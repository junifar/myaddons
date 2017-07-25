from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError

class report_absen_wizard(models.TransientModel):
    _name = 'hr.employee.report.absent.wizard'
    _description = 'Report Absent Priodicaly'

    company_id = fields.Many2one('res.company', required=True)
    report_type = fields.Selection(selection=[('Harian', 'Harian'), ('Bulanan', 'Bulanan'), ('Custom', 'Custom')],
                                   required=True, string="Report Type", default="Harian")
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
    date_filter = fields.Date(string="Tanggal")
    date_filter_from = fields.Date(string="Dari Tanggal")
    date_filter_to = fields.Date(string="Hingga Tanggal")

    def _print_data(self, data):
        return self.env['report'].with_context(landscape=False).get_action(self,
                                                                           'prasetia_hr.report_absen',
                                                                           data=data)

    @api.multi
    def show_data(self):
        self.ensure_one()
        self_obj = self.env.context

        data = {}
        data['ids'] = self_obj.get('active_ids', [])
        data['model'] = self_obj.get('active_model', 'ir.ui.menu')
        data['form'] = self.read([
                        'company_id', 'report_type',
                        'month_filter', 'year_filter',
                        'date_filter', 'date_filter_from',
                        'date_filter_to'])[0]
        return self._print_data(data)
