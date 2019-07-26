# -*- coding: utf-8 -*-

#################################################################################
# Systems Services, Inc.
# Desc: To extend contacts module 
#################################################################################

{
    "name":  "SSI Partner Mods",
    "summary":  "Partner modifications",
    "category":  "SSI",
    "version":  "1.0",
    "sequence":  1,
    "author":  "Systems Services, Inc.",
    "website":  "https://ssibtr.com",
    "depends":  [
        'contacts',
    ],
    "data":  [
        'views/ssi_contacts.xml',

    ],
    "application":  False,
    "installable":  True,
    "auto_install":  False,
}
