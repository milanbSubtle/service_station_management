from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    vehicle = fields.Many2one(comodel_name="vehicle", string="Vehicle")
