from odoo import api, fields, models, _
from datetime import timedelta


class VehicleServiceRecordsWizard(models.TransientModel):
    _name = "vehicle.service.records.wizard"

    vehicle = fields.Many2one(comodel_name="vehicle", string="Vehicle", required=True)

    def print_vehicle_service_records(self):
        vehicle_id = self.vehicle.id
        data_list = []

        service_records = self.env['service.management'].search([('vehicle', '=', vehicle_id)])
        for service_record in service_records:
            service_record_details = {}
            record_line_details = []
            line_detail = {}

            service_date = service_record.date_time + timedelta(hours=5, minutes=30)

            record_lines = service_record.record_lines
            sequence = service_record.sequence_no
            service_record_details['sequence_no'] = sequence
            service_record_details['service_date'] = service_date

            for record_line in record_lines:
                line_detail = {}
                line_service_type = record_line.service_type.name
                line_detail['service_type'] = line_service_type
                line_detail['qty'] = record_line.quantity
                line_detail['value'] = record_line.total_price
                record_line_details.append(line_detail)
            service_record_details['line_info'] = record_line_details
            data_list.append(service_record_details)

        data = {
            'form_data': self.read()[0],
            'data_list': data_list
        }

        return self.env.ref('service_station_management.vehicle_service_records_action').report_action(self, data=data)
