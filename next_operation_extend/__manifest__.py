# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Next Operation Customization',
    'version': '12.0.1.0.0',
    'author': 'Aktiv Software',
    'depends': ['mrp','mrp_workorder'],
    'description': 'If all the preceding work orders is not finish then system will raise a warning,else the system will work with the normal flow.',
    'website': '',
    'data': [
            'views/mrp_routing_workcenter_view.xml'
    ],
    'category': 'Manufacturing',
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'qweb': [
    ],
}