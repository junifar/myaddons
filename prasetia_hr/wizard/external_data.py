import base64
from datetime import datetime

from odoo.exceptions import ValidationError
from xlrd import XLRDError
from xlrd import open_workbook
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class import_external_data(models.TransientModel):
    _name = 'external.import'

    name = fields.Char(string='Nama File', required=True)
    bin_file = fields.Binary(string="Upload File", required=True)

    @api.multi
    def _insert_sample(self, context):
        print '===work insert_sample==='
        _logger.critical('CREATE test')
        employee_organization_area_pool = self.env['hr.employee.organization.area']
        values = {
            'name': 'APA'
        }
        print employee_organization_area_pool.create(values)

        employee_attendance_pool = self.env['hr.employee.attendance']
        values = {
            'employee_id': 1,
            'name': '2017-07-25'
        }
        print values
        print employee_attendance_pool.create(values)
        print '===saved triggere==='
        return None

    @api.multi
    def show_data(self):
        print '===999==='
        context = self._context
        self._insert_sample(context)
        print context['current_id']
        try:
            workbook = open_workbook(file_contents=base64.decodestring(self.bin_file))
            # sheet = workbook.sheets()[0]
            for s in workbook.sheets():
                values = []
                for row in range(s.nrows):
                    col_value = []
                    for col in range(s.ncols):
                        value = s.cell(row, col).value
                        try:
                            value = str(int(value))
                        except:
                            pass
                        col_value.append(value)
                    values.append(col_value)
                print values
            print "===  TEST  ==="
            print self.name
            print "===TEST END==="
        except XLRDError:
            raise ValidationError(_('File Bukan Tipe Excell'))
            pass
        return None
