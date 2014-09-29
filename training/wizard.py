'''
Created on 29 sept. 2014

@author: openerp
'''

from openerp import models, fields, api, exceptions


class Wizard(models.TransientModel):
    _name = "training.wizard"
    
    def _get_default_traing(self):
        import pprint; pprint.pprint(self._context)
        trainings = self.env[self._context.get('active_model')].browse(self._context.get('active_ids'))
        return trainings
    
    unit_price = fields.Float()
    training_ids =  fields.Many2many('training.training', default=_get_default_traing)
    
    @api.multi
    def save(self):
        self.ensure_one()
        self.training_ids.write({'unit_price' : self.unit_price})
        #for training in self.training_ids:
        #    training.unit_price = self.unit_price
        return {}
        