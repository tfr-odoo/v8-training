from openerp.tests.common import TransactionCase, SingleTransactionCase
from openerp.exceptions import Warning, ValidationError
cache = {}

class TestTeacher(SingleTransactionCase):
    
    def test_01_create_course(self):
        course_env = self.env['openacademy.course']
        cache['course_id'] = course_env.create({
            'name' : 'Api V8',
            'description' : 'Api v8 description',
            'responsible_id' : self.ref('base.user_demo'),
        }).id
        
    def test_02_create_course_constrains(self):
        course_env = self.env['openacademy.course']
        with self.assertRaises(ValidationError):
            course_env.create({
                'name' : 'Api',
                'description' : 'Api',
                'responsible_id' : self.ref('base.user_demo'),
            })
            
    def test_03_attendee_count(self):
        course_id = cache['course_id']
        attendee_count_old = self.env['openacademy.course'].browse(course_id).attendee_count
        session_env = self.env['openacademy.session']
        cache['session_id'] = session_env.create({
            'name' : 'Session septembre',
            'seats' : 10,
            'instructor_id'  : self.ref('base.main_partner'),
            'course_id' : course_id,
        }).id
        
        attendee_count = self.env['openacademy.course'].browse(course_id).attendee_count
        self.assertEqual(attendee_count, attendee_count_old)
        
    def test_04_copy_course(self):
        course_id = cache['course_id']
        self.env['openacademy.course'].browse(course_id).copy()
        self.env['openacademy.course'].browse(course_id).copy()
        
    def test_05_onchange_session(self):
        session_id = cache['session_id']
        session = self.env['openacademy.session'].browse(session_id)
        session.onchange_remaining_seats()
        
        session.seats = -1
        session.onchange_remaining_seats()
        

    def test_05_workflow_session(self):
        session_id = cache['session_id']
        session = self.env['openacademy.session'].browse(session_id)
        session.action_draft()
        self.assertEqual(session.state, "draft")
        session.action_confirm()
        self.assertEqual(session.state, "confirmed")
        session.action_done()
        self.assertEqual(session.state, "done")