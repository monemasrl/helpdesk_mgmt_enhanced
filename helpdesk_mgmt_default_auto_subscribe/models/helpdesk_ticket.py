###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import api, models


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

        if ticket.stage_id.mail_template_id:
            ticket.stage_id.mail_template_id.send_mail(
                ticket.id, force_send=True, notif_layout=False
            )

        return ticket
