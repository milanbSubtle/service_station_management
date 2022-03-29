# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Service Station Management System',
    'version' : '1',
    'depends': [
        'base',
        'product'
    ],
    'data': [
        'views/vehicle_view.xml',
        'views/service_management_view.xml',
        'views/menu.xml',
        'security/ir.model.access.csv'
    ],


    'installable': True,
    'application': True,

}
