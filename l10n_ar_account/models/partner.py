# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
import re


class res_partner(models.Model):
    _inherit = 'res.partner'

    responsability_id = fields.Many2one(
        'afip.responsability', 'Resposability')
    iibb = fields.Char('Gross Income', size=64)
    start_date = fields.Date('Start-up Date')
    other_afip_document_class_ids = fields.Many2many(
        'afip.document_class',
        'res_partner_afip_doc_class_rel',
        'partner_id', 'document_class_id',
        string='Other AFIP Documents',
        domain=[('document_type', '=', 'in_document')],
        help='Set here if this partner can issue other documents further\
        than invoices, credit notes and debit notes'
        )

    @api.onchange('document_number', 'document_type_id')
    def onchange_document(self):
        mod_obj = self.env['ir.model.data']
        if self.document_number and ('afip.document_type', self.document_type_id.id) == mod_obj.get_object_reference('l10n_ar_invoice', 'dt_CUIT'):
            document_number = re.sub('[^1234567890]', '', str(self.document_number))
            self.vat = 'AR%s' % document_number
            self.document_number = document_number
