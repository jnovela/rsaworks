# -*- coding: utf-8 -*-

#################################################################################
# Systems Services, Inc.
# Desc: To extend maintenance module to add fields to equipment
#################################################################################

{
    'name': 'SSI Leads',
    'summary': "Adds Leads module to Odoo.",
    'version': '1.0.1',
    'category': 'SSI',
    'author': 'Systems Services, Inc. '
              'Kristenn Quemener ',
    'website': 'https://ssibtr.com',
    "depends":  [
        'base',
        'res',
        'crm',
    ],
    # 'data': [
    #     'security/ir.model.access.csv',
    #     'views/add_default_job_stages.xml',
    #     'views/jobs.xml',
    #     'views/wo.xml',
    # ],
    'installable': True,
    'application': True,
}
