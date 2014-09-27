import time

from openerp.osv import fields
from openerp.osv.osv import Model

class Course(Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Course'

    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for course in self.browse(cr, uid, ids, context=context):
            num=0
            for session in course.session_ids:
                num+=len(session.attendee_ids)
            res[course.id] = num
        return res

    _columns = {
        'name': fields.char('Course Title', 128, required=True),
        'description': fields.text('Description'),
        'responsible_id': fields.many2one('res.users', string='Responsible',ondelete='set null',
            select=True),
        'session_ids': fields.one2many('openacademy.session', 'course_id', 'Session'),
        'attendee_count': fields.function(_get_attendee_count,
                                type='integer', string='attendee Count',
                                method=True),
        'color': fields.integer('Color Index'),
    }

    #Check whether the course title and the course description are not the same
    def _check_description(self, cr, uid, ids, context=None):
        courses = self.browse(cr, uid, ids, context=context)
        for course in courses:
            if course.name == course.description:
                return False
        return True

    _constraints = [(_check_description, 'Please use a different description',
        ['name','description'])]

    #Check that the course title has an unique name
    _sql_constraints = [('unique_name', 'unique(name)','Course Title must be unique')]

    def copy(self, cr, uid, id, defaults, context=None):
        previous_name = self.browse(cr, uid, id, context=context).name
        new_name = 'Copy of %s' % previous_name
        list=self.search(cr, uid, [('name','like',new_name)], context=context)
        if len(list) > 0:
            new_name='%s (%s)' % (new_name,len(list)+1)
        defaults['name'] = new_name
        return super(Course, self).copy(cr, uid, id, defaults, context=context)

class Session(Model):
    _name = 'openacademy.session'
    _description = 'OpenAcademy Session'

    def _get_remaining_seats_percent(self, seats, attendee_list):
       return ((100.0 * (seats - len(attendee_list)))/ seats) if seats else 0

    def _remaining_seats_percent(self, cr, uid, ids, field, arg, context=None):
        #count the percentage of remaining seats
        sessions = self.browse(cr, uid, ids, context=context)
        result = {}
        for session in sessions :
            result[session.id] = self._get_remaining_seats_percent(session.seats,
                                                              session.attendee_ids)
        return result

    def onchange_remaining_seats(self,cr,uid,ids,seats,attendee_ids):
        res = {
            'value': {
                'remaining_seats_percent':
                    self._get_remaining_seats_percent(seats, attendee_ids)
            }
        }
        if seats < 0:
            res['warning'] = {
                'title': 'Warning',
                'message': 'You cannot have negative seats',
            }
        return res

    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for session in self.browse(cr, uid, ids, context=context):
            res[session.id] = len(session.attendee_ids)
        return res

    _columns = {
        'name': fields.char('Session Title', 128, required=True),
        'start_date': fields.date('Start Date'),
        'duration': fields.float('Duration', digits=(6,2), help="Duration in days"),
        'seats':fields.integer('Seats number'),
        'attendee_ids': fields.one2many('openacademy.attendee',
            'session_id', 'Attendees',),
        'remaining_seats_percent':fields.function(_remaining_seats_percent,
                                                  method=True,type='float',
                                                  string='Remaining seats',),
        'instructor_id': fields.many2one('res.partner', 'Instructor',
            domain=['|',('instructor','=',True),
                        ('category_id.name', 'in', ('Teacher Level 1','Teacher Level 2'))
                   ]),
        'course_id':fields.many2one('openacademy.course', 'Course',
            required=True, ondelete='cascade'),
        'active': fields.boolean('Active'),
        'attendee_count': fields.function(_get_attendee_count,
                                type='integer', string='attendee Count',
                                ),
        'state':fields.selection([('draft','Draft'),('confirmed','Confirmed'),
             ('done','Done')],'Status',readonly=True,
                                 required=True),
    }

    _defaults = {
        'start_date': lambda *a : time.strftime('%Y-%m-%d'),
        'active': True,
        'state': 'draft',
    }

    def action_draft(self,cr,uid,ids,context=None):
        #set to "draft" state
        return self.write(cr,uid,ids,{'state':'draft'},context=context)

    def action_confirm(self,cr,uid,ids,context=None):
        #set to "confirmed" state
        return self.write(cr,uid,ids,{'state':'confirmed'},context=context)

    def action_done(self,cr,uid,ids,context=None):
        #set to "done" state
        return self.write(cr,uid,ids,{'state':'done'},context=context)

class Attendee(Model):
    _name = 'openacademy.attendee'
    _rec_name = 'partner_id'

    _columns =  {
        'name': fields.char('Attendee Name', 128),
        'partner_id': fields.many2one('res.partner','Partner',required=True,
            ondelete="cascade"),
        'session_id': fields.many2one('openacademy.session','Session',
            required=True,
            ondelete="cascade"),
    }

