# -*- coding: utf-8 -*-
from odoo import http

# class Prasetia-hr(http.Controller):
#     @http.route('/prasetia-hr/prasetia-hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/prasetia-hr/prasetia-hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('prasetia-hr.listing', {
#             'root': '/prasetia-hr/prasetia-hr',
#             'objects': http.request.env['prasetia-hr.prasetia-hr'].search([]),
#         })

#     @http.route('/prasetia-hr/prasetia-hr/objects/<model("prasetia-hr.prasetia-hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('prasetia-hr.object', {
#             'object': obj
#         })