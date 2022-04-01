from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class Bay(models.Model):
    _name = 'bay'
    _description = 'Bay Details'
    _rec_name = 'code'

    name = fields.Char(string="Bay Name", required=True)
    code = fields.Char(string="Bay Code")
    state = fields.Selection([('available', 'Available'), ('reserved', 'Reserved')])

    # avoid duplicate bay codes
    _sql_constraints = [
        ('code_duplicate_error', 'unique(code)', "Bay Code cannot be duplicated !"),
    ]
    # avoid duplicate bay codes
    # @api.onchange('code')
    # def _check_bay_code(self):
    #     bay_objects = self.env['bay'].search([])
    #     for bay_object in bay_objects:
    #         if self.code == bay_object.code:
    #             raise UserError(_('Bay Code cannot be duplicated'))

