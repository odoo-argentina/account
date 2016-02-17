# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models
# import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):

    """
    En argentina como no se diferencian los impuestos en las facturas, excepto
    el IVA, agrego campos que ignoran el iva solamenta a la hora de imprimir
    los valores.
    """

    _inherit = "account.invoice.line"
