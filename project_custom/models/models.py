# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class project_custom(models.Model):
#     _name = 'project_custom.project_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class project_test(models.Model):
    _name = "project.sample"

    name = fields.Char('Name')
    image = fields.Binary("Image")