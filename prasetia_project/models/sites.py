from odoo import models, fields, api


class site(models.Model):
    _name = 'project.site'
    _description = 'Site Information'

    name = fields.Char(required=True, string='Site Name')
    site_alias1 = fields.Char(string='Site Alias 1')
    site_alias2 = fields.Char(string='Site Alias 2')
    area_id = fields.Many2one('project.area', string='Area', required=False)
    island_id = fields.Many2one('project.island', string='Pulau', required=False)
    province_id = fields.Many2one('project.province', string='Provinsi', required=False)
    city_id = fields.Many2one('project.city', string='Kabupaten / Kota', required=False)
    field_type_id = fields.Many2one('projects.field,type', string='Field Type', required=False)
    site_id_prasetia = fields.Char(string='Site ID Prasetia', default='<Auto Generate ID>')
    site_id_customer = fields.Char(string='Site ID Customer')
    customer_id = fields.Many2one('res.partner', string='Customer', required=False, domain=[('customer', '=', True)])
    tower_type_id = fields.Many2one('project.tower.type', required=False, string='Tower Type')
    tinggi_tower_id = fields.Many2one('project.tinggi.tower', required=False, string='Tinggi Tower')
    address = fields.Text(string="Address", required=True)

    @property
    def __str__(self):
        return self.site_id_prasetia + ' - ' + self.name


class area(models.Model):
    _name = 'project.area'
    _description = 'Area Information'

    name = fields.Char(String='Area', required=True)


class island(models.Model):
    _name = 'project.island'
    _description = 'Island Information'

    name = fields.Char(string='Pulau', required=True)


class province(models.Model):
    _name = 'project.province'
    _description = 'Province Information'

    name = fields.Char(string='Provinsi', required=True)
    island_id = fields.Many2one('project.island', string='Pulau', required=False)


class city(models.Model):
    _name = 'project.city'
    _description = 'City Information'

    name = fields.Char(string='Kabupaten / Kota', required=True)
    province_id = fields.Many2one('project.province', string='Provinsi', required=False)
    island_id = fields.Many2one('project.island', string='Pulau', required=False)


class field_type(models.Model):
    _name = 'project.field.type'
    _description = 'Field type Information'

    name = fields.Char(string='Field Type', required=True)

class projects(models.Model):
    _inherit = 'project.project'

    site_id = fields.Many2one('project.site', string='Site ID', required=False)