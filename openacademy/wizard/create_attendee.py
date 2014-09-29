from openerp import models, fields, api

class attendee_memory(models.TransientModel):
    _name = 'openacademy.attendee.memory'

    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner','Partner',required=True)
    wiz_id = fields.Many2one('openacademy.create.attendee.wizard',)
    

class create_attendee_wizard(models.TransientModel):
    _name = 'openacademy.create.attendee.wizard'

    def _get_active_session(self):
        return self.env.context.get('active_id')

    session_id = fields.Many2one('openacademy.session', 'Session', required=True, default=_get_active_session)
    attendee_ids = fields.One2many('openacademy.attendee.memory', 'wiz_id','Attendees')

    @api.one
    def action_add_attendee(self):
        attendee_pool = self.env['openacademy.attendee']
        for attendee in self.attendee_ids:
            attendee_pool.create({'name':attendee.name,
                                       'partner_id':attendee.partner_id.id,
                                       'session_id':self.session_id.id} )

        return {} # An empty dictionary will close the wizard.

