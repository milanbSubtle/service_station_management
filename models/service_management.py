from odoo import api, fields, models, _
from datetime import datetime, timedelta


class ServiceManagement(models.Model):
    _name = "service.management"
    _description = "Service Management Details"

    vehicle = fields.Many2one(comodel_name="vehicle", string="Vehicle", required=True)
    customer = fields.Many2one(comodel_name="res.partner", string="Customer")
    date_time = fields.Datetime(string="Date and Time", default=datetime.now())
    estimated_date_time = fields.Datetime(string="Estimated Date and Time", compute="_compute_estimate_date_time")
    record_lines = fields.One2many(comodel_name="service.record.lines", inverse_name="service_management_id",
                                   string="Record Lines")

    @api.onchange("vehicle")
    def _set_customer(self):
        self.customer = self.vehicle.owner

    @api.depends("date_time")
    def _compute_estimate_date_time(self):
        for record in self:
            record.estimated_date_time = (record.date_time + timedelta(hours=2))


class ServiceRecordLines(models.Model):
    _name = "service.record.lines"
    _description = "Service Record Lines"

    service_type = fields.Many2one(comodel_name="product.product", string="Service Type", required=True)
    service_management_id = fields.Many2one(comodel_name="service.management")
    quantity = fields.Float(string="Quantity", default="1")
    price = fields.Float(string="Price")
    total_price = fields.Monetary(currency_field='res_currency', string="Total Price", readonly=True)
    res_currency = fields.Many2one(comodel_name='res.currency'
                                                '', default=lambda self: self.env.company.currency_id)
    total = fields.Float(string="Total", compute="_calculate_total")

    @api.onchange('service_type')
    def _onchange_price(self):
        self.price = self.service_type.list_price

    @api.onchange('price', 'quantity')
    def _onchange_total_price(self):
        self.total_price = self.price * self.quantity

    @api.depends('total')
    def _calculate_total(self):
        for total_record in self:
            total_record += self.total_price
