# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Teacher(models.Model):
    _name = 'form_api.teacher'

    name = fields.Char(string="Name", required=True)
    publication_ids = fields.One2many('form_api.bibliography', 'teacher_id', string="Publications")
    
    
class Bibiography(models.Model):
    
    _name = 'form_api.bibliography'
    
    name        = fields.Char("Name", required=True)
    description = fields.Text("Description")
    date        = fields.Date("Publication Date", default=fields.Date.today)
    nb_sold     = fields.Integer("Number sold", default=10)
    teacher_id  = fields.Many2one('form_api.teacher',string="Teacher", ondelete='set null', index=True)
    year        = fields.Integer(compute='_get_year', readonly=True, store=True)
    unit_price  = fields.Float()
    total_sold  = fields.Float()
    user_id     = fields.Many2one("res.users", compute='_get_current_user')
    
    @api.one
    @api.depends('date')
    def _get_year(self):
        self.year = fields.Date.from_string(self.date).year
    
    @api.onchange('nb_sold', 'unit_price')
    def _on_change_total_sold(self):
        self.total_sold = self.unit_price * self.nb_sold
    
    @api.one
    @api.constrains('nb_sold')
    def _check_nb_sold(self):
        if self.nb_sold < 0:
            raise ValidationError("Cannot have a negative number of sold item")
        
    @api.one
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Bibiography, self).copy(default)
    
    @api.multi
    def _get_current_user(self):
        for pub in self:
            pub.user_id = self.env.user
            
    @api.one
    def reset(self):
        print "Print name", self.name
        self.name = "reset"
        self.description = "reset"
        self.unit_price = 0
        self.nb_sold = 0
        import pprint
        print pprint.pprint(self._columns)
        print pprint.pprint(self._fields)
        
        user_model = self.env['res.users']
        print user_model.login #False it's an empty record set
        print user_model.partner_id.name # don't be affraid to chain event with an empty record set
        print self.reset._api
        print self.reset._orig
        
        
    @api.cr_uid_context
    def default_get(self, cr, uid, fields, context=None):
        res = super(Bibiography, self).default_get(cr, uid, fields, context=context)
        res.update({'unit_price' : 2.0})
        return res
    
    @api.multi
    def unlink(self):
        for pub in self:
            print "delete", pub.name
        return super(Bibiography, self).unlink()
    
    @api.multi
    def read(self, fields, load='_classic_read'):
        res = super(Bibiography, self).read(fields)
        for r in res:
            if 'name' in fields:
                r['name'] = "MODIFICATION"
        return res
        