from datetime import datetime

from odoo import models, fields, api, exceptions, _


class Barang(models.Model):
    _name = "prasetia.barang"
    name = fields.Char(required=True, string='Nama Barang')
    qty = fields.Integer(string='Quantity')
