###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import _, fields, models


class HelpdeskEnhancedSla(models.Model):
    _name = "helpdesk.enhanced.sla"
    _description = "Helpdesk Enhanced SLA"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(required=True, default=lambda self: _("New"), copy=False)

    team_id = fields.Many2one(
        string="Team",
        comodel_name="helpdesk.ticket.team",
        ondelete="restrict",
    )
