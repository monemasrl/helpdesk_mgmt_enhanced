###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import _, fields, models


class HelpdeskEnhancedAction(models.Model):
    _name = "helpdesk.enhanced.action"
    _description = "Helpdesk Enhanced Action"

    _rec_name = "name"
    _order = "name ASC"

    name = fields.Char(required=True, default=lambda self: _("New"), copy=False)

    group_id = fields.Many2one(
        string="Group/Role",
        comodel_name="res.groups",
        ondelete="restrict",
    )

    state_id = fields.Many2one(
        string="Ticket stage",
        comodel_name="helpdesk.ticket.stage",
        required=True,
        ondelete="restrict",
    )

    next_state_id = fields.Many2one(
        string="Next Ticket stage",
        comodel_name="helpdesk.ticket.stage",
        ondelete="restrict",
    )

    timer_action = fields.Selection(
        selection=[("none", "None"), ("start", "Start"), ("stop", "Stop")],
    )

    priority_action = fields.Selection(
        selection=[("none", "None"), ("inc", "Increase"), ("dec", "Decrease")],
    )

    mail_template_id = fields.Many2one(
        string="Mail Template",
        comodel_name="mail.template",
        ondelete="restrict",
    )

    activation = fields.Selection(
        string="activation",
        selection=[
            ("oncreate", "On Create"),
            ("onupdate", "On Update"),
            ("user", "User"),
            ("timer", "Timer"),
        ],
    )

    timer_type = fields.Selection(selection=[("before", "Before"), ("after", "After")])

    time = fields.Integer()

    time_unit = fields.Selection(selection=[("hours", "Hours"), ("days", "Days")])
