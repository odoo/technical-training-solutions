# -*- coding: utf-8 -*-
# More info at https://www.odoo.com/documentation/master/reference/module.html

{
    "name": "Real Estate",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
        "report/estate_reports.xml",
        "report/estate_report_views.xml",
    ],
    "demo": [
        "data/estate_demo.xml"
    ],
    "application": True,
}
