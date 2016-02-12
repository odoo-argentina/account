# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning
import openerp.addons.decimal_precision as dp
import re
import logging
_logger = logging.getLogger(__name__)


class account_invoice(models.Model):
    _inherit = "account.invoice"

    currency_rate = fields.Float(
        string='Currency Rate',
        copy=False,
        digits=(16, 4),
        # TODO make it editable, we hace to change move create method
        readonly=True,
        )
    # TODO chequear si los necesitamos
    # invoice_number = fields.Integer(
    #     compute='_get_invoice_number',
    #     string=_("Invoice Number"),
    #     )
    # point_of_sale = fields.Integer(
    #     compute='_get_invoice_number',
    #     string=_("Point Of Sale"),
    #     )
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
    #     string='Responsability',
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
            product_types = set(
                [x.product_id.type for x in self.invoice_line_ids if x.product_id])
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
            if self.afip_document_class_id.afip_code in [19, 20, 21]:
                # TODO verificar esto, como par expo no existe 3 y existe 4
                # (otros), considermaos que un mixto seria el otros
                if afip_concept == '3':
                    afip_concept = '4'
        self.afip_concept = afip_concept

    # @api.one
    # def _get_taxes_and_prices(self):
    #     """
    #     """

    #     vat_taxes = self.tax_line.filtered(
    #         lambda r: (
    #             r.tax_code_id.type == 'tax' and r.tax_code_id.tax == 'vat'))
    #     vat_amount = sum(
    #         vat_taxes.mapped('amount'))
    #     vat_base_amount = sum(
    #         vat_taxes.mapped('base'))

    #     not_vat_taxes = self.tax_line - vat_taxes

    #     other_taxes_amount = sum(
    #         (self.tax_line - vat_taxes).mapped('amount'))

    #     vat_exempt_amount = sum(vat_taxes.filtered(
    #             lambda r: r.tax_code_id.afip_code == 2).mapped('base'))

    #     vat_untaxed = sum(vat_taxes.filtered(
    #             lambda r: r.tax_code_id.afip_code == 1).mapped('base'))

    #     if self.vat_discriminated:
    #         printed_amount_untaxed = self.amount_untaxed
    #         printed_taxes = self.tax_line
    #     else:
    #         printed_amount_untaxed = self.amount_total
    #         printed_taxes = False

    #     self.printed_amount_untaxed = printed_amount_untaxed
    #     self.printed_tax_ids = printed_taxes
    #     self.printed_amount_tax = self.amount_total - printed_amount_untaxed
    #     self.vat_tax_ids = vat_taxes
    #     self.not_vat_tax_ids = not_vat_taxes
    #     self.vat_amount = vat_amount
    #     self.other_taxes_amount = other_taxes_amount
    #     self.vat_exempt_amount = vat_exempt_amount
    #     self.vat_untaxed = vat_untaxed
    #     self.vat_base_amount = vat_base_amount

    # @api.one
    # @api.depends('afip_document_number', 'number')
    # def _get_invoice_number(self):
    #     """ Funcion que calcula numero de punto de venta y numero de factura
    #     a partir del document number. Es utilizado principalmente por el modulo
    #     de vat ledger citi
    #     """
    #     # TODO mejorar estp y almacenar punto de venta y numero de factura por separado
    #     # de hecho con esto hacer mas facil la carga de los comprobantes de compra
    #     str_number = self.afip_document_number or self.number or False
    #     if str_number and self.state not in ['draft', 'proforma', 'proforma2', 'cancel']:
    #         if self.afip_document_class_id.afip_code in [33, 99, 331, 332]:
    #             point_of_sale = '0'
    #             # leave only numbers and convert to integer
    #             invoice_number = str_number
    #         # despachos de importacion
    #         elif self.afip_document_class_id.afip_code == 66:
    #             point_of_sale = '0'
    #             invoice_number = '0'
    #         elif "-" in str_number:
    #             splited_number = str_number.split('-')
    #             invoice_number = splited_number.pop()
    #             point_of_sale = splited_number.pop()
    #         elif "-" not in str_number and len(str_number) == 12:
    #             point_of_sale = str_number[:4]
    #             invoice_number = str_number[-8:]
    #         else:
    #             raise Warning(_(
    #                 'Could not get invoice number and point of sale for invoice id %i') % (
    #                     self.id))
    #         self.invoice_number = int(re.sub("[^0-9]", "", invoice_number))
    #         self.point_of_sale = int(re.sub("[^0-9]", "", point_of_sale))

    # TODO we should use same field for in or out invoices
    # _sql_constraints = [
    #     ('number_supplier_invoice_number',
    #         'unique(supplier_invoice_number, type, partner_id, company_id)',
    #      'Supplier Invoice Number must be unique per Supplier and Company!'),
    # ]

    # TODO analizar
    # @api.one
    # @api.constrains('supplier_invoice_number', 'partner_id', 'company_id')
    # def _check_reference(self):
    #     if self.type in ['out_invoice', 'out_refund'] and self.reference and self.state == 'open':
    #         domain = [('type', 'in', ('out_invoice', 'out_refund')),
    #                   # ('reference', '=', self.reference),
    #                   ('document_number', '=', self.document_number),
    #                   ('journal_document_class_id.afip_document_class_id', '=',
    #                    self.journal_document_class_id.afip_document_class_id.id),
    #                   ('company_id', '=', self.company_id.id),
    #                   ('id', '!=', self.id)]
    #         invoice_ids = self.search(domain)
    #         if invoice_ids:
    #             raise Warning(_(
    #                 'Supplier Invoice Number must be unique per Supplier'
    #                 ' and Company!'))

    # @api.multi
    # def check_argentinian_invoice_taxes(self):
    #     """
    #     We make theis function to be used as a constraint but also to be called
    #     from other models like vat citi
    #     """
    #     # only check for argentinian localization companies
    #     _logger.info('Running checks related to argentinian documents')

    #     # we consider argentinian invoices the ones from companies with
    #     # localization = argentina and that belongs to a journal with
    #     # use_documents
    #     argentinian_invoices = self.filtered(
    #         lambda r: (
    #             r.localization == 'argentina' and r.use_documents))
    #     if not argentinian_invoices:
    #         return True

    #     # check invoice tax has code
    #     without_tax_code = self.env['account.invoice.tax'].search([
    #         ('invoice_id', 'in', argentinian_invoices.ids),
    #         ('tax_code_id', '=', False),
    #         ])
    #     if without_tax_code:
    #         raise Warning(_(
    #             "You are using argentinian localization and there are some "
    #             "invoices with taxes that don't have tax code, tax code is "
    #             "required to generate this report. Invoies ids: %s" % (
    #                 without_tax_code.mapped('invoice_id.id'))))

    #     # check codes has argentinian tax attributes configured
    #     tax_codes = argentinian_invoices.mapped('tax_line.tax_code_id')
    #     unconfigured_tax_codes = tax_codes.filtered(
    #         lambda r: not r.type or not r.tax or not r.application)
    #     if unconfigured_tax_codes:
    #         raise Warning(_(
    #             "You are using argentinian localization and there are some tax"
    #             " codes that are not configured. Tax codes ids: %s" % (
    #                 unconfigured_tax_codes.ids)))

    #     # Check invoice with amount
    #     invoices_without_amount = self.search([
    #         ('id', 'in', argentinian_invoices.ids),
    #         ('amount_total', '=', 0.0)])
    #     if invoices_without_amount:
    #         raise Warning(_('Invoices ids %s amount is cero!') % (
    #             invoices_without_amount.ids))

    #     # Check invoice requiring vat

    #     # out invoice must have vat if are argentinian and from a company with
    #     # responsability that requires vat
    #     sale_invoices_with_vat = self.search([(
    #         'id', 'in', argentinian_invoices.ids),
    #         ('type', 'in', ['out_invoice', 'out_refund']),
    #         ('company_id.partner_id.responsability_id.vat_tax_required_on_sales_invoices',
    #             '=', True)])

    #     # check purchase invoice has supplier invoice number
    #     purchase_invoices = argentinian_invoices.filtered(
    #         lambda r: r.type in ('in_invoice', 'in_refund'))
    #     purchase_invoices_without_sup_number = purchase_invoices.filtered(
    #         lambda r: (not r.supplier_invoice_number))
    #     if purchase_invoices_without_sup_number:
    #         raise Warning(_(
    #             "Some purchase invoices don't have supplier nunmber.\n"
    #             "Invoices ids: %s" % purchase_invoices_without_sup_number.ids))

    #     # purchase invoice must have vat if document class letter has vat
    #     # discriminated
    #     purchase_invoices_with_vat = purchase_invoices.filtered(
    #         lambda r: (
    #             r.afip_document_class_id.document_letter_id.vat_discriminated))

    #     invoices_with_vat = (
    #         sale_invoices_with_vat + purchase_invoices_with_vat)

    #     for invoice in invoices_with_vat:
    #         # we check vat base amount is equal to amount untaxed
    #         # usamos una precision de 0.1 porque en algunos casos no pudimos
    #         # arreglar pbñe,as de redondedo 
    #         if abs(invoice.vat_base_amount - invoice.amount_untaxed) > 0.1:
    #             raise Warning(_(
    #                 "Invoice ID: %i\n"
    #                 "Invoice subtotal (%.2f) is different from invoice base"
    #                 " vat amount (%.2f)" % (
    #                     invoice.id,
    #                     invoice.amount_untaxed,
    #                     invoice.vat_base_amount)))

    #     # check purchase invoices that can't have vat. We check only the ones
    #     # with document letter because other documents may have or not vat tax
    #     purchase_invoices_without = purchase_invoices.filtered(
    #         lambda r: (
    #             r.afip_document_class_id.document_letter_id and
    #             not r.afip_document_class_id.document_letter_id.vat_discriminated))
    #     for invoice in purchase_invoices_without:
    #         if invoice.vat_tax_ids:
    #             raise Warning(_(
    #                 "Invoice ID %i shouldn't have any vat tax" % invoice.id))

    #     # Check except vat invoice
    #     afip_exempt_codes = ['Z', 'X', 'E', 'N', 'C']
    #     for invoice in argentinian_invoices:
    #         special_vat_taxes = invoice.tax_line.filtered(
    #             lambda r: r.tax_code_id.afip_code in [1, 2, 3])
    #         if (
    #                     special_vat_taxes
    #                     and invoice.fiscal_position.afip_code
    #                     not in afip_exempt_codes):
    #             raise Warning(_(
    #                 "If there you have choose a tax with 0, exempt or untaxed,"
    #                 " you must choose a fiscal position with afip code in %s. "
    #                 "Invoice id %i" % (
    #                     afip_exempt_codes, invoice.id)))

    # @api.multi
    # def action_move_create(self):
    #     """
    #     We add currency rate on move creation so it can be used by electronic
    #     invoice later on action_number
    #     """
    #     self.check_argentinian_invoice_taxes()
    #     for inv in self:
    #         inv.currency_rate = inv.currency_id.compute(
    #                 1., inv.company_id.currency_id)
    #     return super(account_invoice, self).action_move_create()
