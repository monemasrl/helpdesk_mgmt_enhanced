###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging
from datetime import datetime

from odoo import fields, models

_logger = logging.getLogger(__name__)


class HelpdeskEnhancedSla(models.Model):
    _inherit = "helpdesk.sla"

    team_id = fields.Many2one(
        string="Team",
        comodel_name="helpdesk.ticket.team",
        ondelete="restrict",
    )

    action_ids = fields.Many2many(
        string="Actions",
        comodel_name="helpdesk.enhanced.action",
        relation="helpdesk_enhanced_action_helpdesk_sla_rel",
        column1="helpdesk_enhanced_action_id",
        column2="helpdesk_sla_id",
    )

    def check_sla(self):
        _logger.debug("CHECK SLA")
        for team in self.team_id:
            _logger.debug("Team: {}".format(self.team_id))
            if team.ticket_ids:
                _logger.debug("Calling check_ticket_sla")
                self.check_ticket_sla(team.ticket_ids)

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
