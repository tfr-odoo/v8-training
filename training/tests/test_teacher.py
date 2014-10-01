from openerp.tests.common import TransactionCase, SingleTransactionCase

cache = {}

class TestTeacher(SingleTransactionCase):
    
    
    """ V7 style test """
    def test_10_create_teacher(self):
        """Test Create teacher
        """
        cr, uid = self.cr, self.uid
        context = {}
        teacher_reg = self.registry('academy.teachers')
        
        #self.ref('module.xml_id')
        #partner_rec = self.browse_ref('base.main_partner')
        #print partner_rec.name
        
        old_t_ids = teacher_reg.search(cr, uid, [('name', '=', 'Thibault')], context=context)
        cache['teacher_id'] = teacher_reg.create(cr, uid, {
            'name' : 'Thibault',
            'first_name' : 'Francois',
            'age' : 32
        })
        self.assertTrue(cache['teacher_id'], "Teacher creation return False")
        t_ids = teacher_reg.search(cr, uid, [('name', '=', 'Thibault')], context=context)
        self.assertEqual(len(old_t_ids) + 1, len(t_ids), 'Thibault not found')
        
        
        
    """ V8 style test """
    def test_11_create_teacher(self):
        """Test Create teacher  """
        cache['teacher_id']
        env = self.env['academy.teachers']
        teacher = env.search([('name', '=', 'Thibault')])
        self.assertTrue(teacher, "Teacher not found")
        