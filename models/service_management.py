from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class ServiceManagement(models.Model):
    _name = "service.management"
    _description = "Service Management Details"

    vehicle = fields.Many2one(comodel_name="vehicle", string="Vehicle", required=True)
    customer = fields.Many2one(comodel_name="res.partner", string="Customer")
    date_time = fields.Datetime(string="Date and Time", default=datetime.now())
    estimated_date_time = fields.Datetime(string="Estimated Date and Time", compute="_compute_estimate_date_time")
    record_lines = fields.One2many(comodel_name="service.record.lines", inverse_name="service_management_id",
                                   string="Record Lines")
    total = fields.Float(string="Total", compute="_calculate_total")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('invoice', 'Invoiced'), ('paid', 'Paid')],
                             string="States", default="draft")
    actual_end_date = fields.Datetime(string="Actual Date and Time")
    sequence_no = fields.Char(string="Service Reference", default=lambda self: _('New'))

    # bay lines
    bay_lines = fields.One2many(comodel_name="bay", inverse_name="bay_records_id", string="Bay Lines")

    @api.onchange("vehicle")
    def _set_customer(self):
        self.customer = self.vehicle.owner

    @api.depends("date_time")
    def _compute_estimate_date_time(self):
        for record in self:
            record.estimated_date_time = (record.date_time + timedelta(hours=2))

    # calculate total
    @api.depends('record_lines')
    def _calculate_total(self):
        for record in self:
            total = 0
            service_lines = record.record_lines
            for service_line in service_lines:
                total += service_line.total_price
            record.total = total

    def action_confirm(self):
        sequence = self.env['ir.sequence'].next_by_code('service_sequence') or _('New')
        self.write({'state': 'confirm', 'sequence_no': sequence})

    def action_invoice(self):
        if self.actual_end_date:
            self.write({'state': 'invoice'})
        else:
            raise UserError(_('Please update actual end date'))


class ServiceRecordLines(models.Model):
    _name = "service.record.lines"
    _description = "Service Record Lines"

    service_type = fields.Many2one(comodel_name="product.product", string="Service Type", required=True)
    service_management_id = fields.Many2one(comodel_name="service.management")
    quantity = fields.Float(string="Quantity", default="1")
    price = fields.Float(string="Price")
    total_price = fields.Monetary(currency_field='res_currency', string="Total Price", readonly=True)
    res_currency = fields.Many2one(comodel_name='res.currency', default=lambda self: self.env.company.currency_id)

    @api.onchange('service_type')
    def _onchange_price(self):
        self.price = self.service_type.list_price

    @api.onchange('price', 'quantity')
    def _onchange_total_price(self):
        self.total_price = self.price * self.quantity
