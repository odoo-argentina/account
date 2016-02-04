# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, api, models, _
from openerp.exceptions import Warning


class account_fiscal_position(models.Model):
    _inherit = 'account.fiscal.position'

    afip_code = fields.Char(
        'AFIP Code',
        help='For eg. This code will be used on electronic invoice and citi '
        'reports'
        )


class account_journal_afip_document_class(models.Model):
    _name = "account.journal.afip_document_class"
    _description = "Journal Afip Documents"
    _rec_name = 'afip_document_class_id'
    _order = 'journal_id desc, sequence, id'

    afip_document_class_id = fields.Many2one(
        'afip.document_class',
        'Document Type',
        required=True,
        ondelete='cascade',
        )
    sequence_id = fields.Many2one(
        'ir.sequence',
        'Entry Sequence',
        help="This field contains the information related to the numbering of the documents entries of this document type."
        )
    journal_id = fields.Many2one(
        'account.journal',
        'Journal',
        required=True,
        ondelete='cascade',
        )
    journal_type = fields.Selection(
        related='journal_id.type',
        readonly=True,
        )
    sequence = fields.Integer(
        'Sequence',
        )
    point_of_sale_id = fields.Many2one(
        related='journal_id.point_of_sale_id',
        redaonly=True,
        )


class account_journal(models.Model):
    _inherit = "account.journal"

    journal_document_class_ids = fields.One2many(
        'account.journal.afip_document_class',
        'journal_id',
        'Documents Classes',
        )
    point_of_sale_id = fields.Many2one(
        'afip.point_of_sale',
        'Point of sale',
        help='On use documents and sales journals is mandatory, con purchase journal is optional and only used to easily manage journals'
        )
    use_documents = fields.Boolean(
        'Use Documents?'
        )

    @api.onchange('company_id', 'type')
    def change_company(self):
        if self.type != 'sale':
            self.use_documents = False
        else:
            self.use_documents = self.company_id.use_argentinian_localization

    @api.multi
    def get_journal_letter(self):
        """Function to be inherited by afip ws fe"""
        self.ensure_one()
        responsability = self.company_id.responsability_id
        if self.type in ['sale', 'sale_refund']:
            letters = responsability.issued_letter_ids
        elif self.type in ['purchase', 'purchase_refund']:
            letters = responsability.received_letter_ids
        return letters

    @api.one
    @api.constrains(
        'point_of_sale_id',
        'company_id',
        'use_documents',
        )
    def check_document_classes(self):
        """
        Tricky constraint to create documents on journal
        """
        if not self.use_documents:
            return True

        letters = self.get_journal_letter()

        other_purchase_doc_types = ['in_document', 'ticket']

        if self.type in ['purchase', 'sale']:
            document_types = ['invoice', 'debit_note']
            # for purchase we add other documents with letter
            if self.type == 'purchase':
                document_types += other_purchase_doc_types
        elif self.type in ['purchase_refund', 'sale_refund']:
            document_types = ['credit_note']

        document_classes = self.env['afip.document_class'].search([
            ('document_type', 'in', document_types),
            ('document_letter_id', 'in', letters.ids)])

        # for purchases we add in_documents and ticket whitout letters
        # TODO ver que no hace falta agregar los tickets aca porque ahora le
        # pusimos al tique generico la letra x entonces ya se agrega solo.
        # o tal vez, en vez de usar letra x, lo deberiamos motrar tambien como
        # factible por no tener letra y ser tique
        if self.type == 'purchase':
            document_classes += self.env['afip.document_class'].search([
                ('document_type', 'in', other_purchase_doc_types),
                ('document_letter_id', '=', False)])

        # take out documents that already exists
        document_classes = document_classes - self.mapped(
                    'journal_document_class_ids.afip_document_class_id')

        sequence = 10
        for document_class in document_classes:
            sequence_id = False
            if self.type in ['sale', 'sale_refund']:
                # Si es nota de debito nota de credito y same sequence, no creamos la secuencia, buscamos una que exista
                if document_class.document_type in [
                        'debit_note', 'credit_note'] and self.point_of_sale_id.document_sequence_type == 'same_sequence':
                    journal_documents = self.journal_document_class_ids.search(
                        [('afip_document_class_id.document_letter_id', '=', document_class.document_letter_id.id),
                         ('journal_id.point_of_sale_id', '=', self.point_of_sale_id.id)])
                    sequence_id = journal_documents and journal_documents[0].sequence_id.id or False
                else:
                    sequence_id = self.env['ir.sequence'].create({
                        'name': self.name + ' - ' + document_class.name,
                        'padding': 8,
                        'prefix': "%04i-" % (self.point_of_sale_id.number),
                        'company_id': self.company_id.id,
                    }).id
            self.journal_document_class_ids.create({
                'afip_document_class_id': document_class.id,
                'sequence_id': sequence_id,
                'journal_id': self.id,
                'sequence': sequence,
            })
            sequence += 10

    @api.one
    @api.constrains('point_of_sale_id', 'company_id')
    def _check_company_id(self):
        """
        Check point of sale and journal company
        """
        if self.point_of_sale_id and self.point_of_sale_id.company_id != self.company_id:
            raise Warning(_('The company of the point of sale and of the \
                journal must be the same!'))
