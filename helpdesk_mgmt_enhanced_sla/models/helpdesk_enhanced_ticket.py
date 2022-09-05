###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    sla_id = fields.Many2one(
        comodel_name="helpdesk.sla",
        string="SLA",
        required=True,
        help="The SLA this ticket is attached to",
    )

    sla_status = fields.Selection(
        string="SLA status",
        selection=[("running", "Running"), ("stopped", "Stopped")],
        default="stopped",
    )

    sla_last_applied_action = fields.Char(
        string="Last Applied Action",
    )

    @api.onchange("sla_id")
    def _onchange_sla_id(self):
        self.team_id = self.sla_id.team_id
        self.sla_id.check_sla()
