# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api
# from openerp.exceptions import Warning


class account_fiscal_position(models.Model):
    _inherit = 'account.fiscal.position'

    afip_code = fields.Char(
        'AFIP Code',
        help='For eg. This code will be used on electronic invoice and citi '
        'reports'
        )


class account_journal(models.Model):
    _inherit = "account.journal"

    point_of_sale_type = fields.Selection([
        ('manual', 'Manual'),
        ('preprinted', 'Preprinted'),
        ('online', 'Online'),
        # Agregados por otro modulo
        # ('electronic', 'Electronic'),
        # ('fiscal_printer', 'Fiscal Printer'),
        ],
        'Point Of Sale Type',
        default='manual',
        required=True,
        )
    point_of_sale_number = fields.Integer(
        'Point Of Sale Number',
        required=True,
        help='On Argentina Localization with use documents and sales journals '
        ' is mandatory'
        )

    @api.onchange(
        'type', 'localization', 'use_documents', 'point_of_sale_number',
        'point_of_sale_type', 'sequence_id')
    def change_to_set_name_and_code(self):
        """
        We only set name and code if not sequence_id
        """
        if (
                self.type == 'sale' and
                self.localization == 'argentina' and
                self.use_documents and
                not self.sequence_id
                ):
            if self.point_of_sale_type == 'manual':
                name = 'Manual'
            elif self.point_of_sale_type == 'preprinted':
                name = 'Preimpresa'
            elif self.point_of_sale_type == 'online':
                name = 'Online'
            elif self.point_of_sale_type == 'electronic':
                name = 'Electronica'
            self.name = '%s %s %04d' % (
                'Ventas', name, self.point_of_sale_number)
            self.code = 'V%04d' % (self.point_of_sale_number)
