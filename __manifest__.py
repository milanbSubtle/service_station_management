# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Service Station Management System',
    'version': '1',
    'depends': [
        'base',
        'product',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_view.xml',
        'views/service_management_view.xml',
        'views/account_move_views.xml',
        'views/bay_view.xml',
        'views/vehicle_details_view.xml',
        'views/menu.xml',
        'report/vehicle_details_template.xml'
    ],


    'installable': True,
    'application': True,

}
