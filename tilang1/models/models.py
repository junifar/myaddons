# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class openerp/addons/maintenance(models.Model):
#     _name = 'openerp/addons/maintenance.openerp/addons/maintenance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100