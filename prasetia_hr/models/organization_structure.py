from odoo import models, fields, api
from odoo.exceptions import ValidationError


class organization_structure(models.Model):
    _name = "hr.employee.organization.structure"
    _parent_name = "parent_id"

    name = fields.Char(string="Role", required=True)
    parent_id = fields.Many2one('hr.employee.organization.structure', 'Parent Role', index=True, ondelete='cascade')
    child_id = fields.One2many('hr.employee.organization.structure', 'parent_id', 'Child Categories')

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