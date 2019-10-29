# -*- coding: utf-8 -*-

#################################################################################
# Systems Services, Inc.
# Desc: To extend accounting modules
#################################################################################

{
    'name': 'SSI Accounting',
    'summary': "Accounting Customizations",
    'version': '1.0.1',
    'category': 'SSI',
    'author': 'Systems Services, Inc. '
              'Chad Thompson',
    'website': 'https://ssibtr.com',
    "depends":  [
        'base',
        'account',
    ],
    'data': [
        # 'views/ssi_accounting.xml',
        'report/ssi_gross_margin_report.xml',
    ],
    'installable': True,
    'application': False,
}
