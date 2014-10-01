from openerp import models, fields, api, exceptions


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Course'



    name = fields.Char('Course Title', required=True)
    description = fields.Text('Description')
    responsible_id = fields.Many2one('res.users', 
                                     string='Responsible', 
                                     ondelete='set null',
                                     index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string='Session')
    attendee_count = fields.Integer(compute='_get_attendee_count', string='attendee Count', store=True)
    color = fields.Integer('Color Index')
    
    @api.one
    @api.depends('session_ids.attendee_ids')
    def _get_attendee_count(self):
        num = 0
        for session in self.session_ids:
            num+=len(session.attendee_ids)
        self.attendee_count = num
        
    @api.one
    @api.constrains('name', 'description')
    def _check_description(self):
        if self.name == self.description:
            raise exceptions.Warning('Please use a different description')

    #Check that the course title has an unique name
    _sql_constraints = [('unique_name', 'unique(name)','Course Title must be unique')]

    @api.one
    def copy(self, defaults=None):
        defaults = dict(defaults or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        defaults['name'] = new_name
        return super(Course, self).copy(defaults)

class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'OpenAcademy Session'

    name = fields.Char('Session Title', required=True)
    start_date = fields.Date('Start Date', default=lambda *a: fields.Date.today())
    duration = fields.Float('Duration', digits=(6,2), help="Duration in days")
    seats = fields.Integer('Seats number')
    attendee_ids = fields.One2many('openacademy.attendee', 'session_id', 'Attendees',)
    remaining_seats_percent = fields.Float(compute='_get_attendee_count', string='Remaining seats',)
    instructor_id =  fields.Many2one('res.partner', 'Instructor', domain=['|',('instructor','=',True),
                        ('category_id.name', 'in', ('Teacher Level 1','Teacher Level 2'))
                   ])
    course_id = fields.Many2one('openacademy.course', 'Course', required=True, ondelete='cascade')
    active = fields.Boolean('Active', default=True)
    attendee_count = fields.Integer(compute='_get_attendee_count',
                                string='attendee Count', store=True
                                )
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),
             ('done','Done')], string='Status',readonly=True,
                                 required=True, default='draft')
    @api.one 
    @api.depends('attendee_ids', 'seats')   
    def _get_attendee_count(self):
        print "Call _get_attendee_count"
        self.attendee_count = len(self.attendee_ids)
        self.remaining_seats_percent = ((100.0 * (self.seats - self.attendee_count))/ self.seats) if self.seats else 0
    
    
    @api.one
    @api.onchange('seats', 'attendee_ids')
    def onchange_remaining_seats(self):
        self.remaining_seats_percent = ((100.0 * (self.seats - self.attendee_count))/ self.seats) if self.seats else 0
        res = {}
        if self.seats < 0:
            res['warning'] = {
                'title': 'Warning',
                'message': 'You cannot have negative seats',
            }
        return res

    
    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'
        
    @api.one
    def action_done(self):
        self.state = 'done'

class Attendee(models.Model):
    _name = 'openacademy.attendee'
    _rec_name = 'partner_id'

    name = fields.Char('Attendee Name')
    partner_id = fields.Many2one('res.partner','Partner', required=True, ondelete="cascade")
    session_id = fields.Many2one('openacademy.session','Session', required=True, ondelete="cascade")


