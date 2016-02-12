# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def _get_localizations(self):
        localizations = super(ResCompany, self)._get_localizations()
        localizations.append(['argentina', 'Argentina'])
        return localizations

    iibb = fields.Char(
        related='partner_id.iibb',
        )
    start_date = fields.Date(
        related='partner_id.start_date',
        )
    # TODO ver si lo movemos a account_document
    # journal_ids = fields.One2many(
    #     'account.journal',
    #     'company_id',
    #     'Journals'
    #     )
