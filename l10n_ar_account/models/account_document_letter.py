# -*- coding: utf-8 -*-
from openerp import models, fields


class AccountDocumentLetter(models.Model):
    _name = 'account.document.letter'
    _description = 'Account Document Letter'

    name = fields.Char(
        'Name',
        required=True
        )
    document_type_ids = fields.One2many(
        'account.document.type',
        'document_letter_id',
        'Document Types'
        )
    issuer_ids = fields.Many2many(
        'afip.responsible.type',
        'account_document_letter_responsible_issuer_rel',
        'document_letter_id',
        'afip_responsible_type_id',
        'Issuers',
        )
    receptor_ids = fields.Many2many(
        'afip.responsible.type',
        'account_document_letter_responsible_receptor_rel',
        'document_letter_id',
        'afip_responsible_type_id',
        'Receptors',
        )
    active = fields.Boolean(
        'Active',
        default=True
        )
    included_tax_group_ids = fields.Many2many(
        'account.tax.group',
        'account_document_letter_tax_group_rel',
        'document_letter_id', 'tax_group_id',
        'Included Tax Groups',
        help='For documents of this letter, include this taxes of this group '
        'on invoices amounts'
        )
    # taxes_discriminated = fields.Boolean(
    #     'Taxes Discriminated on Invoices?',
    #     help="If True, the taxes will be discriminated on invoice report.")

    _sql_constraints = [('name', 'unique(name)', 'Name must be unique!'), ]
