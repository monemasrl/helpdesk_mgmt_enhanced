###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import _, fields, models


class HelpdeskEnhancedSlaRule(models.Model):
    _name = "helpdesk.enhanced.sla.rule"
    _description = "Helpdesk Enhanced SLA Rule"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(required=True, default=lambda self: _("New"), copy=False)

    sla_id = fields.Many2one(
        comodel_name="helpdesk.enhanced.sla", string="SLA", required=True
    )
    stage_id = fields.Many2one(comodel_name="helpdesk.ticket.stage", string="Stage")
    days = fields.Integer(default=0, required=True)
    hours = fields.Integer(default=0, required=True)
    note = fields.Char()
