# -*- coding: utf-8 -*-
from openerp import models, api, fields
# from openerp.exceptions import Warning


class AccountDocmentType(models.Model):
    _inherit = 'account.document.type'

    document_letter_id = fields.Many2one(
        'account.document.letter',
        'Document Letter'
        )

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

    @api.multi
    def get_taxes_included(self):
        """
        In argentina we include taxes depending on document letter
        """
        self.ensure_one()
        if self.localization == 'argentina':
            included_tax_groups = (
                self.document_letter_id.included_tax_group_ids)
            if included_tax_groups:
                return self.env['account.tax'].search(
                    [('tax_group_id', 'in', included_tax_groups.ids)])
        else:
            return super(AccountDocmentType, self).get_taxes_included()
