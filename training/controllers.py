# -*- coding: utf-8 -*-
from openerp import http

class Training(http.Controller):
    
    @http.route('/smile', auth='public', 
                type="http", method=['GET', 'POST'], 
                website=True)
    def index(self, **kw):
        teachers_env = http.request.env['academy.teachers']
        
        return http.request.render('training.index', {
            'teachers': teachers_env.search([]),
        })
        
    @http.route('/smile/<int:teacher_id>/', auth='public', website=True)
    def teacher(self, teacher_id):
        teachers_env = http.request.env['academy.teachers']
        page = 'training.view_teacher'
        if not teachers_env.search([('id', '=', teacher_id)]):
            page = 'website.page_404'
        return http.request.render(page, {
            'teacher': teachers_env.browse(teacher_id),
            'return_path' : 'smile'
        })
    
    @http.route('/smile/<string(length=2):lang>/', auth='public', website=True)
    def lang(self, lang):
        return '<h1>{}</h1> lang'.format(lang)
    
    
    @http.route('/smile/<model("academy.teachers"):teacher>/', auth='public', website=True)
    def teacher_simple(self, teacher):
        return http.request.render('training.view_teacher', {
            'teacher': teacher,
            'return_path' : 'smile'
        })
