###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import fields, models


class ResConfigSettings(models.Model):
    _inherit = "res.config.settings"

    send_mail_on_create = fields.Boolean(
        string="Email on ticket creation",
        config_parameter="helpdesk.send_mail_on_create",
    )
    on_create_mail_template_id = fields.Many2one(
        string="Email Template",
        comodel_name="mail.template",
        ondelete="restrict",
        help="Select or create the mail template used for new ticket notification",
        config_parameter="helpdesk.on_create_mail_template_id",
    )

    def set_values(self):
        return super(ResConfigSettings, self).set_values()
