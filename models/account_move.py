from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    vehicle = fields.Many2one(comodel_name="vehicle", string="Vehicle")

    @api.onchange('partner_id')
    def _set_vehicle_domain(self):
        customer = self.partner_id.id
        vehicle_ids = self.env['vehicle'].search([('owner', '=', customer)])
        if vehicle_ids:
            vehicle_id_list = vehicle_ids.ids
            return {
                'domain': {'vehicle': [('id', 'in', vehicle_id_list)]}
            }
