###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import fields, models


class HelpdeskEnhancedSla(models.Model):
    _inherit = "helpdesk.sla"

    team_id = fields.Many2one(
        string="Team",
        comodel_name="helpdesk.ticket.team",
        ondelete="restrict",
    )
