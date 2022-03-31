from odoo import api, fields, models, _


class Bay(models.Model):
    _name = 'bay'
    _description = 'Bay Details'

    name = fields.Char(string="Bay Name", required=True)
    code = fields.Char(string="Bay Code")

    bay_records_id = fields.Many2one(comodel_name="service.management")
