# -*- coding: utf-8 -*-

#################################################################################
# Systems Services, Inc. 
# Desc: To extend maintenance module to add fields to equipment
#################################################################################

{
  "name"                 :  "SSI Maintenance Mods",
  "summary"              :  "Add feilds to the equipment table",
  "category"             :  "SSI",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Systems Services, Inc.",
  "website"              :  "https://ssibtr.com",
  "depends"              :  [
                             'maintenance',
                            ],
  "data"                 :  [
                              'views/ssi_maintenance.xml',
                            ],
  "application"          :  False,
  "installable"          :  True,
  "auto_install"         :  False,
}