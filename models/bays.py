from odoo import api, fields, models, _


class Bay(models.Model):
    _name = 'bay'
    _description = 'Bay Details'
    _rec_name = 'code'

    name = fields.Char(string="Bay Name", required=True)
    code = fields.Char(string="Bay Code")
