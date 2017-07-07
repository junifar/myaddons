# -*- coding: utf-8 -*-
from openerp import http

# class Openerp/addons/maintenance(http.Controller):
#     @http.route('/openerp/addons/maintenance/openerp/addons/maintenance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openerp/addons/maintenance/openerp/addons/maintenance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openerp/addons/maintenance.listing', {
#             'root': '/openerp/addons/maintenance/openerp/addons/maintenance',
#             'objects': http.request.env['openerp/addons/maintenance.openerp/addons/maintenance'].search([]),
#         })

#     @http.route('/openerp/addons/maintenance/openerp/addons/maintenance/objects/<model("openerp/addons/maintenance.openerp/addons/maintenance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openerp/addons/maintenance.object', {
#             'object': obj
#         })

class TilangController(http.Controller):
	@http.route('/contoh')
	def index(self, **kw):

		SIMPLE_TEMPLATE = """
			<html>
				<head>
					<link rel="stylesheet" href="/tilang/static/src/css/style.css"/>
				</head>
				<body>
					<h1>Hello World</h1>
				</body>				
			</html>

		"""
		return SIMPLE_TEMPLATE
		# return "Hello, World"