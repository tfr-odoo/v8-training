# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
from openerp.tools.translate import _
from openerp.osv import fields as old_fields, osv, orm


class TrainingParent(models.Model):
    _name = 'training.old'
    _columns = {
        'name' : old_fields.char("Name old", readonly=True),
                
    }

class Training(models.Model):
    _name = 'training.training'
    _inherit = 'training.old'

    def _get_default_qty(self):
        print self
        print "get default qty"
        return 10
    
    def _get_default_total(self):
        print "get default total"
        print self
        #self.qty = self.unit_price * self.qty
        return 10.0
    
        
    name = fields.Char(required=True, readonly=False)
    description = fields.Char("Note")
    unit_price = fields.Float(copy=False)
    #qty = fields.Integer(default=_get_default_qty)
    qty = fields.Integer()
    total = fields.Float(compute='_get_total', 
                         #inverse='_inverse_total',
                         #search='_search_total',
                         store=True, required=False, default=_get_default_total)
    total_store = fields.Float(compute='_get_total_store', 
                         #inverse='_inverse_total',
                         #search='_search_total',
                         store=True, required=False, default=_get_default_total)
    client_id = fields.Many2one(comodel_name='res.partner', index=True)
    client_name = fields.Char(related='client_id.name', store=False)
    
    @api.onchange('client_id')
    def _onchange_partner(self):
        #self.name = '%s (%s)' % (self.name, self.client_id.name)
        self.name = '{} ({})'.format(self.name or '', self.client_id.name or '')
        return { 'warning' : {'title' : "a title", 'message' : 'a message'}}
        
        
    
    @api.one
    @api.depends('qty', 'unit_price')
    def _get_total(self):
        self.total = self.qty * self.unit_price
        
    @api.one
    @api.depends('qty', 'unit_price')
    def _get_total_store(self):
        self.total_store = self.qty * self.unit_price
        
    @api.one
    def _inverse_total(self):
        self.unit_price = self.total / self.qty
        
    def _search_total(self):
        return [('unit_price', '>', 0.0)]
        
    @api.multi
    def click(self):
        self.ensure_one()
        self = self[0]
        record = self.search([])
        record = self.browse()
        
        self.env
        
        
        #si plus d'un élément 
        self.name = "Click"
        self.description = "J'ai clické"
        #préféré
        self.write({'name' : 'name', 'description' :  'j\'ai clické'})
        
        if record:
            print "not null"
        else:
            print "null"
        print record
        #for tr in self:
        #    print tr.name
    
    
        #lire premier élément de la liste
        recset = self.search([])
        print "list of ids", recset.ids
        print "tuple of ids", recset._ids
        #print 'first element of the list', recset.name
        
        admin = self.env['res.partner'].browse(1)
        agrolait = self.env['res.partner'].browse(7)
        #not allowed
        admin.parent_id = 7
        admin.parent_id = agrolait
        
        
        #dict
        #self.env.context['foo'] = "bar"
        new_context = dict(self.env.context)
        new_context['foo'] = "bar"
        self.with_env(self.env(self.env.cr, self.env.uid, new_context))
        
        recs = self.with_context(new_context)
        recs = recs.with_context(key='value')
        
        recs = recs.sudo(2)
        #recs.write({'name' : 'name', 'description' :  'j\'ai clické'})
        self.env.invalidate_all()
        
    @api.multi
    def write(self, vals):
        print "#### write ####"
        print self.env.uid
        import pprint
        pprint.pprint(self.env.context)
        print len(self)
        return super(Training, self).write(vals)
    
    @api.model
    @api.returns('self')
    def create(self, vals):
        return models.Model.create(self, vals)
    
    _sql_constraints = [('unique_name', 'UNIQUE(name)', "Name should be unique ")]
     
    @api.one
    @api.constrains('qty')
    def _check_qty(self):
        if self.qty < 0.0:
            raise exceptions.Warning(_("QTY error"), _("QTY cannot be negative"))
    
