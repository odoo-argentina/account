# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import re
import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    currency_rate = fields.Float(
        string='Currency Rate',
        copy=False,
        digits=(16, 4),
        # TODO make it editable, we hace to change move create method
        readonly=True,
        )
    document_letter_id = fields.Many2one(
        related='document_type_id.document_letter_id',
        )
    afip_responsible_type_id = fields.Many2one(
        'afip.responsible.type',
        string='AFIP Responsible Type',
        readonly=True,
        copy=False,
        )
    invoice_number = fields.Integer(
        compute='_get_invoice_number',
        string="Invoice Number",
        )
    point_of_sale_number = fields.Integer(
        compute='_get_invoice_number',
        string="Point Of Sale",
        )
    # TODO chequear si los necesitamos
    # # no gravado en iva
    # vat_untaxed = fields.Float(
    #     compute="_get_taxes_and_prices",
    #     digits=dp.get_precision('Account'),
    #     string=_('VAT Untaxed')
    #     )
    # # exento en iva
    # vat_exempt_amount = fields.Float(
    #     compute="_get_taxes_and_prices",
    #     digits=dp.get_precision('Account'),
    #     string=_('VAT Exempt Amount')
    #     )
    # # von iva
    # vat_amount = fields.Float(
    #     compute="_get_taxes_and_prices",
    #     digits=dp.get_precision('Account'),
    #     string=_('VAT Amount')
    #     )
    # # von iva
    # vat_base_amount = fields.Float(
    #     compute="_get_taxes_and_prices",
    #     digits=dp.get_precision('Account'),
    #     string=_('VAT Base Amount')
    #     )
    # other_taxes_amount = fields.Float(
    #     compute="_get_taxes_and_prices",
    #     digits=dp.get_precision('Account'),
    #     string=_('Other Taxes Amount')
    #     )
    # vat_tax_ids = fields.One2many(
    #     compute="_get_taxes_and_prices",
    #     comodel_name='account.invoice.tax',
    #     string=_('VAT Taxes')
    #     )
    # not_vat_tax_ids = fields.One2many(
    #     compute="_get_taxes_and_prices",
    #     comodel_name='account.invoice.tax',
    #     string=_('Not VAT Taxes')
    #     )
    # supplier_invoice_number = fields.Char(
    #     copy=False,
    #     )
    afip_incoterm_id = fields.Many2one(
        'afip.incoterm',
        'Incoterm',
        readonly=True,
        states={'draft': [('readonly', False)]}
        )
    # formated_vat = fields.Char(
    #     string='responsible',
    #     related='commercial_partner_id.formated_vat',
    #     )
    point_of_sale_type = fields.Selection(
        related='journal_id.point_of_sale_type',
        readonly=True,
        )
    # estos campos los agregamos en este modulo pero en realidad los usa FE
    # pero entendemos que podrian ser necesarios para otros tipos, por ahora
    # solo lo vamos a hacer requerido si el punto de venta es del tipo
    # electronico
    afip_concept = fields.Selection(
        compute='_get_concept',
        # store=True,
        selection=[('1', 'Producto / Exportación definitiva de bienes'),
                   ('2', 'Servicios'),
                   ('3', 'Productos y Servicios'),
                   ('4', '4-Otros (exportación)'),
                   ],
        string="AFIP concept",
        )
    afip_service_start = fields.Date(
        string='Service Start Date'
        )
    afip_service_end = fields.Date(
        string='Service End Date'
        )

    @api.one
    @api.depends('document_number', 'number')
    def _get_invoice_number(self):
        """ Funcion que calcula numero de punto de venta y numero de factura
        a partir del document number. Es utilizado principalmente por el modulo
        de vat ledger citi
        """
        # TODO mejorar estp y almacenar punto de venta y numero de factura por
        # separado, de hecho con esto hacer mas facil la carga de los
        # comprobantes de compra
        str_number = self.document_number or self.number or False
        if str_number and self.state not in [
                'draft', 'proforma', 'proforma2', 'cancel']:
            if self.document_type_id.code in [33, 99, 331, 332]:
                point_of_sale = '0'
                # leave only numbers and convert to integer
                invoice_number = str_number
            # despachos de importacion
            elif self.document_type_id.code == 66:
                point_of_sale = '0'
                invoice_number = '0'
            elif "-" in str_number:
                splited_number = str_number.split('-')
                invoice_number = splited_number.pop()
                point_of_sale = splited_number.pop()
            elif "-" not in str_number and len(str_number) == 12:
                point_of_sale = str_number[:4]
                invoice_number = str_number[-8:]
            else:
                raise Warning(_(
                    'Could not get invoice number and point of sale for '
                    'invoice id %i') % (self.id))
            self.invoice_number = int(
                re.sub("[^0-9]", "", invoice_number))
            self.point_of_sale_number = int(
                re.sub("[^0-9]", "", point_of_sale))

    @api.one
    @api.depends(
        'invoice_line_ids',
        'invoice_line_ids.product_id',
        'invoice_line_ids.product_id.type',
        'localization',
    )
    def _get_concept(self):
        afip_concept = False
        if self.point_of_sale_type in ['online', 'electronic']:
            # exportaciones
            invoice_lines = self.invoice_line_ids
            product_types = set(
                [x.product_id.type for x in invoice_lines if x.product_id])
            consumible = set(['consu', 'product'])
            service = set(['service'])
            mixed = set(['consu', 'service', 'product'])
            # default value "product"
            afip_concept = '1'
            if product_types.issubset(mixed):
                afip_concept = '3'
            if product_types.issubset(service):
                afip_concept = '2'
            if product_types.issubset(consumible):
                afip_concept = '1'
            if self.document_type_id.code in [19, 20, 21]:
                # TODO verificar esto, como par expo no existe 3 y existe 4
                # (otros), considermaos que un mixto seria el otros
                if afip_concept == '3':
                    afip_concept = '4'
        self.afip_concept = afip_concept

    @api.multi
    def get_localization_invoice_vals(self):
        self.ensure_one()
        if self.localization == 'argentina':
            commercial_partner = self.partner_id.commercial_partner_id
            return {'afip_responsible_type_id': (
                    commercial_partner.afip_responsible_type_id.id)}
        else:
            return super(
                AccountInvoice, self).get_localization_invoice_vals()

    @api.multi
    def _get_available_journal_document_types(self):
        """
        This function search for available document types regarding:
        * Journal
        * Partner
        * Company
        * Documents configuration
        If needed, we can make this funcion inheritable and customizable per
        localization
        """
        self.ensure_one()
        if self.localization != 'argentina':
            return super(
                AccountInvoice, self)._get_available_journal_document_types()
        invoice_type = self.type

        journal_document_types = journal_document_type = self.env[
            'account.journal.document.type']

        if invoice_type in [
                'out_invoice', 'in_invoice', 'out_refund', 'in_refund']:

            if self.use_documents:

                letters = self.journal_id.get_journal_letter(
                    counterpart_partner=self.commercial_partner_id)

                domain = [
                    ('journal_id', '=', self.journal_id.id),
                    '|',
                    ('document_type_id.document_letter_id', 'in', letters.ids),
                    ('document_type_id.document_letter_id', '=', False),
                    ]

                # If internal_type in context we try to serch specific document
                # for eg used on debit notes
                internal_type = self._context.get('internal_type', False)
                if internal_type:
                    journal_document_type = journal_document_type.search(
                        domain + [
                            ('document_type_id.internal_type',
                                '=', internal_type)], limit=1)

                # For domain, we search all documents
                journal_document_types = journal_document_types.search(domain)

                # If not specific document type found, we choose another one
                if not journal_document_type and journal_document_types:
                    journal_document_type = journal_document_types[0]

        if invoice_type == 'in_invoice':
            other_document_types = (
                self.commercial_partner_id.other_document_type_ids)

            domain = [
                ('journal_id', '=', self.journal_id.id),
                ('document_type_id',
                    'in', other_document_types.ids),
                ]
            other_journal_document_types = self.env[
                'account.journal.document.type'].search(domain)

            journal_document_types += other_journal_document_types
            # if we have some document sepecific for the partner, we choose it
            if other_journal_document_types:
                journal_document_type = other_journal_document_types[0]

        return {
            'available_journal_document_types': journal_document_types,
            'journal_document_type': journal_document_type,
            }
