# -*- coding: utf-8 -*-

#################################################################################
# Systems Services, Inc.
# Desc: To extend maintenance module to add fields to equipment
#################################################################################

{
    'name': 'Jobs',
    'summary': "Adds jobs module to Odoo.",
    'version': '1.0.1',
    'category': 'SSI',
    'author': 'Systems Services, Inc. '
              'Chad Thompson ',
    'website': 'https://ssibtr.com',
    'depends': ['base'],
    "depends":  [
        'account',
        'base',
        'mrp',
        'mrp_workorder',
        'product',
        'purchase',
        'sale',
        'stock',
        'sale_timesheet',
    ],
    # 'data': [
    #     'security/ir.model.access.csv',
    #     'views/jobs.xml',
    #     ],
    'installable': True,
    'application': True,
}
