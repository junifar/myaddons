# -*- coding: utf-8 -*-
from odoo import http

# class Odoo\myaddons\prasetiaProject(http.Controller):
#     @http.route('/odoo\myaddons\prasetia_project/odoo\myaddons\prasetia_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo\myaddons\prasetia_project/odoo\myaddons\prasetia_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo\myaddons\prasetia_project.listing', {
#             'root': '/odoo\myaddons\prasetia_project/odoo\myaddons\prasetia_project',
#             'objects': http.request.env['odoo\myaddons\prasetia_project.odoo\myaddons\prasetia_project'].search([]),
#         })

#     @http.route('/odoo\myaddons\prasetia_project/odoo\myaddons\prasetia_project/objects/<model("odoo\myaddons\prasetia_project.odoo\myaddons\prasetia_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo\myaddons\prasetia_project.object', {
#             'object': obj
#         })