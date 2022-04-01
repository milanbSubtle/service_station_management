from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class ServiceManagement(models.Model):
    _name = "service.management"
    _description = "Service Management Details"

    vehicle = fields.Many2one(comodel_name="vehicle", string="Vehicle", required=True)
    customer = fields.Many2one(comodel_name="res.partner", string="Customer")
    date_time = fields.Datetime(string="Start Date and Time", default=datetime.now())
    estimated_date_time = fields.Datetime(string="Estimated Date and Time", compute="_compute_estimate_date_time")
    record_lines = fields.One2many(comodel_name="service.record.lines", inverse_name="service_management_id",
                                   string="Record Lines")
    total = fields.Float(string="Total", compute="_calculate_total")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'), ('in_progress', 'In progress'), ('done', 'Done'),
         ('invoice', 'Invoiced'), ('paid', 'Paid')],
        string="States", default="draft")
    actual_end_date = fields.Datetime(string="Actual End Date and Time")
    # sequence number in service management
    sequence_no = fields.Char(string="Service Reference", default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        start_date = vals['date_time']
        end_date = vals['actual_end_date']
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        if start_date_datetime > end_date_datetime:
            raise UserError(_("Actual End Date and Time and Start Date and Time not matching!!"))
        return super(ServiceManagement, self).create(vals)

    def write(self, values):
        if values.get('actual_end_date'):
            actual_end_datetime = datetime.strptime(values.get('actual_end_date'), '%Y-%m-%d %H:%M:%S')
            if self.date_time > actual_end_datetime:
                raise UserError(_("Actual End Date and Time and Start Date and Time not matching!!"))
        return super(ServiceManagement, self).write(values)

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

    def action_in_progress(self):
        service_lines = self.record_lines
        for service_line in service_lines:
            if service_line.bay_lines:
                service_line.bay_lines.write({'state': 'reserved'})
        self.write({'state': 'in_progress'})

    def action_done(self):
        service_lines = self.record_lines
        for service_line in service_lines:
            if service_line.bay_lines:
                service_line.bay_lines.write({'state': 'available'})
        self.write({'state': 'done'})

    def action_invoice(self):
        if self.actual_end_date:
            self.write({'state': 'invoice'})
        else:
            raise UserError(_('Please update actual end date'))

    def action_paid(self):
        self.write({'state': 'paid'})


class ServiceRecordLines(models.Model):
    _name = "service.record.lines"
    _description = "Service Record Lines"

    service_type = fields.Many2one(comodel_name="product.product", string="Service Type", required=True)
    service_management_id = fields.Many2one(comodel_name="service.management")
    quantity = fields.Float(string="Quantity", default="1")
    price = fields.Float(string="Price")
    # total price
    total_price = fields.Monetary(currency_field='res_currency', string="Total Price", readonly=True)
    res_currency = fields.Many2one(comodel_name='res.currency', default=lambda self: self.env.company.currency_id)
    # bay lines in services
    bay_lines = fields.Many2one(comodel_name="bay", string="Bay Lines",
                                domain="[('state', '=', 'available')]")  # bay line code

    @api.onchange('service_type')
    def _onchange_price(self):
        self.price = self.service_type.list_price

    @api.onchange('price', 'quantity')
    def _onchange_total_price(self):
        self.total_price = self.price * self.quantity
