# -*- coding: utf-8 -*-
from openerp import http

# class FormApi(http.Controller):
#     @http.route('/form_api/form_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/form_api/form_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('form_api.listing', {
#             'root': '/form_api/form_api',
#             'objects': http.request.env['form_api.form_api'].search([]),
#         })

#     @http.route('/form_api/form_api/objects/<model("form_api.form_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('form_api.object', {
#             'object': obj
#         })