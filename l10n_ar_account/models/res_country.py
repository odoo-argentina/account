# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    afip_code = fields.Char(
        'Afip Code', size=3
        )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
