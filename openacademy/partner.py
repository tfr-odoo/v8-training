from openerp import models, fields, api, exceptions

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean()
    session_ids = fields.Many2many('openacademy.session', string="Sessions")

