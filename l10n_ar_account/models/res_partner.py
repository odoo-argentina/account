# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    iibb = fields.Char(
        'Gross Income',
        size=64
        )
    start_date = fields.Date(
        'Start-up Date'
        )
