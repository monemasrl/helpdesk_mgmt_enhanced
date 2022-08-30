###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def create(self, vals):
        if not vals.get("partner_id", False):
            partner_email = vals.get("partner_email", False)

            if partner_email:
                partner_ids = [
                    p.id
                    for p in self.env["mail.thread"]._mail_find_partner_from_emails(
                        [partner_email], records=self, force_create=True
                    )
                    if p
                ]

                ticket = super().create(vals)
                ticket.message_subscribe(partner_ids)

                return ticket
        else:
            vals.get("partner_id")
            ticket = super().create(vals)
            ticket.message_subscribe(partner_ids)

            return ticket

        return super().create(vals)
