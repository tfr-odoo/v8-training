# -*- coding: utf-8 -*-

from openerp import http


class formation(http.Controller):
    @http.route('/formation/', auth='public')
    def index(self):
        #Values that will be available in the 
        client_obj = http.request.env['res.partner']
        values = {
            'trainees' : client_obj.search([]),
        }
        # !! complete xml_id of the template module.id even in the same module
        return http.request.render('form_web.index', values)

