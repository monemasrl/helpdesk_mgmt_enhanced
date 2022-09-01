###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.model
    def create(self, vals):
        partner_ids = []
        if not vals.get("partner_id", False):
            partner_email = vals.get("partner_email", False)

            if partner_email:
                partners = [
                    p
                    for p in self.env["mail.thread"]._mail_find_partner_from_emails(
                        [partner_email], records=self, force_create=True
                    )
                    if p
                ]

                for p in partners:
                    partner_ids.append(p.id)
                    vals["partner_id"] = p.id
                    vals["partner_name"] = p.name
                    vals["partner_email"] = p.email

        else:
            partners = self.env["res.partner"].browse([vals.get("partner_id")])
            for p in partners:
                vals["partner_name"] = p.name
                vals["partner_email"] = p.email

            partner_ids = partners.mapped(lambda r: r.id)

        ticket = super().create(vals)
        ticket.message_subscribe(partner_ids)

        send_mail_on_create = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("helpdesk.send_mail_on_create", default=False)
        )

        if send_mail_on_create:
            on_create_mail_template_id = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("helpdesk.on_create_mail_template_id", default=False)
            )

            template_id = self.env["mail.template"].browse(
                [int(on_create_mail_template_id)]
            )
            template_id.send_mail(ticket.id, force_send=True, notif_layout=False)

        return ticket
