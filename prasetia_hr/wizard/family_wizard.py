from openerp import models, fields, api, _
from openerp.osv import orm
from openerp.exceptions import UserError
from datetime import datetime


class family_wizard(orm.TransientModel):
    _name = "family.wizard"
    _description = "Family Print Wizard"

    employee_id = fields.Many2one('hr.employee', required=True)
    date_filter = fields.Date(string="Tanggal Lahir", default=datetime.now())

    @api.multi
    def print_report(self):
        print "===pass phase 999==="
        self.ensure_one()
        self_obj = self.env.context

        data = {}
        data['ids'] = self_obj.get('active_ids', [])
        data['model'] = self_obj.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_filter'])[0]
        # records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].with_context(landscape=False).get_action(self, 'prasetia_hr.family_report',
                                                                           data=data)
        # return None
