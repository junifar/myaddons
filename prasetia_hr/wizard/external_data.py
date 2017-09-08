import base64
from datetime import datetime

from odoo.exceptions import ValidationError
from xlrd import XLRDError
from xlrd import open_workbook
from odoo import models, fields, api, _
from odoo.exceptions import UserError


# import logging
# _logger = logging.getLogger(__name__)


class import_external_data(models.TransientModel):
    _name = 'external.import'

    name = fields.Char(string='Nama File', required=True)
    bin_file = fields.Binary(string="Upload File", required=True)

    @api.multi
    def _insert_sample(self, ctx):
        # _logger.critical('CREATE test')
        employee_attendance_pool = self.env['hr.employee.attendance']
        values = {
            'employee_id': 1,
            'name': ctx['attendance_name'],
            'absen_book_id': ctx['current_id']
        }
        employee_attendance_pool.create(values)
        return None

    @staticmethod
    def _check_str(value):
        try:
            value = str(int(value))
        except:
            pass
        return value

    def _import_process(self):
        try:
            workbook = open_workbook(file_contents=base64.decodestring(self.bin_file))
            sheet = workbook.sheets()[0]
            values = []
            for row in range(sheet.nrows):
                col_values = []
                if row >= 9:
                    if not sheet.cell(row, 7).value == '':
                        value = self._check_str(sheet.cell(row, 1).value)
                        col_values.append(value)

                        value_hour = self._check_str(sheet.cell(row, 7).value)
                        value_minute = self._check_str(sheet.cell(row, 8).value)
                        col_values.append('%s:%s' % (value_hour, value_minute))

                        value_hour = self._check_str(sheet.cell(row, 9).value)
                        value_minute = self._check_str(sheet.cell(row, 10).value)
                        col_values.append('%s:%s' % (value_hour, value_minute))
                        values.append(col_values)
                print values
        except XLRDError:
            raise ValidationError(_('File Bukan Tipe Excel'))

    @api.multi
    def show_data(self):
        # ctx = self._context
        # self._insert_sample(ctx)

        # try:
        #     workbook = open_workbook(file_contents=base64.decodestring(self.bin_file))
        #     # sheet = workbook.sheets()[0]
        #     # for s in workbook.sheets():
        #     #     values = []
        #     #     for row in range(s.nrows):
        #     #         col_value = []
        #     #         for col in range(s.ncols):
        #     #             value = s.cell(row, col).value
        #     #             try:
        #     #                 value = str(int(value))
        #     #             except:
        #     #                 pass
        #     #             col_value.append(value)
        #     #         values.append(col_value)
        #     #     print values
        #     print "===  TEST  ==="
        #     print self.name
        #     print "===TEST END==="
        # except XLRDError:
        #     raise ValidationError(_('File Bukan Tipe Excell'))
        #     pass
        self._import_process()
        return None
