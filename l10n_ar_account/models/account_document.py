# -*- coding: utf-8 -*-
from openerp import models, api
# from openerp.exceptions import Warning


class AccountDocmentType(models.Model):
    _inherit = 'account.document.type'

    @api.multi
    def get_document_sequence_vals(self, journal):
        vals = super(AccountDocmentType, self).get_document_sequence_vals(
            journal)
        if self.localization == 'argentina':
            vals.update({
                'padding': 8,
                'prefix': "%04i-" % (journal.point_of_sale_number),
                })
        return vals
