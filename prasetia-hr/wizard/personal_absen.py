from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class personal_absen(models.TransientModel):
    _name = 'hr.employee.personal.absent'
    _description = 'Show personal absent report'

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

    def _print_data(self, data):
        records = self.env[data['model']].browse(data.get('ids',[]))
        return None

    @api.multi
    def show_data(self):
        self.ensure_one()
        self_obj = self.env.context

        while True:
            try:
                int(self.year_filter)
                break
            except ValueError:
                raise UserError(_("Invalid year input"))

        data = {'ids': self_obj.get('active_ids', []), 'model': self_obj.get('active_model', 'ir.ui.menu'),
                'form': self.read(['employee_id', 'month_filter', 'year_filter'])}
        return self._print_data(data)
