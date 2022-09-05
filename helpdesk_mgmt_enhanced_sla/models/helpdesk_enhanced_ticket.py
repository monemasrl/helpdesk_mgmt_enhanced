###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging
from datetime import datetime

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


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
        _logger.debug("SLA changed")
        self.check_ticket_sla()

    def check_ticket_sla(self):
        # for ticket in ticket_ids.filtered(lambda t: not t.stage_id.closed):
        for ticket in self:
            deadline = ticket.create_date
            working_calendar = ticket.team_id.resource_calendar_id

            if self.days > 0:
                deadline = working_calendar.plan_days(
                    self.days + 1, deadline, compute_leaves=True
                )
                create_date = ticket.create_date

                deadline = deadline.replace(
                    hour=create_date.hour,
                    minute=create_date.minute,
                    second=create_date.second,
                    microsecond=create_date.microsecond,
                )

                deadline_for_working_cal = working_calendar.plan_hours(0, deadline)

                if (
                    deadline_for_working_cal
                    and deadline.day < deadline_for_working_cal.day
                ):
                    deadline = deadline.replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )

            deadline = working_calendar.plan_hours(
                self.hours, deadline, compute_leaves=True
            )
            ticket.sla_deadline = deadline
            if ticket.sla_deadline < datetime.today().now():
                ticket.sla_expired = True
            else:
                ticket.sla_expired = False
