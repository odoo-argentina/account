# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class afip_ws_currency_rate_wizard(models.TransientModel):
    _name = 'afip.ws.currency_rate.wizard'
    _description = 'AFIP WS Currency Rate Wizard'

    currency_id = fields.Many2one(
        'res.currency',
        'Currency',
        required=True,
        )

    @api.multi
    def confirm(self):
        self.ensure_one()
        journal_id = self._context.get('active_id', False)
        if not journal_id:
            raise Warning(_(
                'No Journal Id as active_id on context'))
        journal = self.env[
            'account.journal'].browse(journal_id)
        return journal.get_pyafipws_currency_rate(self.currency_id)
