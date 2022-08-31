{
    "name": "Helpdesk Auto Subscribe",
    "summary": "When the ticket is created the sender is added as follower to the ticket",
    "version": "14.0.1.0.0",
    "author": "Monema S.r.l.",
    "maintainer": "Monema S.r.l.",
    "contributors": ["Andrea Bettarini <bettarini@monema.it>"],
    "website": "https://github.com/OCA/helpdesk",
    "license": "Other OSI approved licence",
    "category": "After-Sales",
    "application": False,
    "depends": ["helpdesk_mgmt", "helpdesk_mgmt_enhanced_base"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
}
