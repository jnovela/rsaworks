# -*- coding: utf-8 -*-

#################################################################################
# Systems Services, Inc.
# Desc: To extend attendance module in order to create detail attendance records
#################################################################################

{
    "name":  "SSI Attendance Mods",
    "summary":  "Attendance Detail model and other modifications",
    "category":  "SSI",
    "version":  "1.0",
    "sequence":  1,
    "author":  "Systems Services, Inc.",
    "website":  "https://ssibtr.com",
    "depends":  [
        'hr_attendance',
    ],
    "data":  [
        'views/ssi_attendace.xml',
        'security/ir.model.access.csv',

    ],
    "application":  False,
    "installable":  True,
    "auto_install":  False,
}
