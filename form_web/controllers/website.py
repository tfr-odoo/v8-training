# -*- coding: utf-8 -*-

from openerp import http


class formation(http.Controller):
    @http.route('/training/', auth='public', website=True)
    def index(self):
        #Values that will be available in the 
        client_obj = http.request.env['res.partner']
        values = {
            'trainees' : client_obj.search([]),
        }
        # !! complete xml_id of the template module.id even in the same module
        return http.request.render('form_web.training', values)
    
    @http.route('/training/<int:id>/', auth='public', website=True)
    def training(self, id):
        client_obj = http.request.env['res.partner']
        trainee = client_obj.browse(id)
        return '<h1>%s</h1>' % trainee.name
    
    @http.route('/trainee/<model("res.partner"):trainee>/', auth='public', website=True)
    def trainee(self, trainee):
        values = {
            'trainee' : trainee,
        }
        return http.request.render('form_web.trainee', values)