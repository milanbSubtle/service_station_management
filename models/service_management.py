from odoo import api, fields, models, _


class ServiceManagement(models.Model):
    _name = "service_management"
    _description = "Service Management Details"

    vehicle = fields.Many2one(comodel_name="vehicle", string="Vehicle", required=True)
    customer = fields.Many2one(comodel_name="res.partner", string="Customer")
