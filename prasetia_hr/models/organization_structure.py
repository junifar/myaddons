from odoo import models, fields, api
from odoo.exceptions import ValidationError


class organization_role(models.Model):
    _name = "hr.employee.organization.role"
    _parent_name = "parent_id"

    name = fields.Char(string="Role", required=True)
    parent_id = fields.Many2one('hr.employee.organization.role', 'Parent Role', index=True, ondelete='cascade')
    child_id = fields.One2many('hr.employee.organization.role', 'parent_id', 'Child Categories')

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive categories.'))
        return True

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]


class organization_structure(models.Model):
    _name = "hr.employee.organization.structure"

    name = fields.Char(string="Division", required=True)
    president = fields.Many2one('hr.employee', required=True, string="President")
    vice_president = fields.Many2one('hr.employee', string="Vice President")
    organization_team_line = fields.One2many('hr.employee.organization.structure.line', 'organization_structure_id',
                                             'Organization Team')

    @api.multi
    def print_data(self):
        self.ensure_one()
        self_obj = self.env.context

        data = {}
        data['ids'] = self_obj.get('active_ids', [])
        data['model'] = self_obj.get('active_model', 'ir.ui.menu')
        print 'Sample'
        return self.env['report'].with_context(landscape=False).get_action(self,
                                                                           'prasetia_hr.report_organization_structure',
                                                                           data=data)


class organization_area(models.Model):
    _name = "hr.employee.organization.area"

    name = fields.Char(string="Area", required=True)


class organization_cluster(models.Model):
    _name = "hr.employee.organization.cluster"

    name = fields.Char(string="Cluster", required=True)


class organization_structure_line(models.Model):
    _name = "hr.employee.organization.structure.line"

    organization_structure_id = fields.Many2one('hr.employee.organization.structure', string="Struktur Divisi")
    name = fields.Many2one('hr.employee', required=True, string="Karyawan")
    organization_role_id = fields.Many2one('hr.employee.organization.role', string="Jabatan")
    cluster_id = fields.Many2one('hr.employee.organization.cluster', string="Cluster")
    area_id = fields.Many2one('hr.employee.organization.area', string="Area")
    customer_id = fields.Many2one('res.partner', string="Customer")
