from odoo import api, fields, models, _


class Vehicle(models.Model):
    _name = "vehicle"
    _description = "Vehicle details"

    name = fields.Char(string="REG Number", required=True)
    manufacture_date = fields.Date(string="Manufacture Date")