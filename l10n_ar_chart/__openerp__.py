# -*- coding: utf-8 -*-
{
    'name': 'Argentina - Plan Contable General',
    'author':   'OpenERP - Team de Localización Argentina',
    'category': 'Localization/Account Charts',
    'website':  'https://launchpad.net/~openerp-l10n-ar-localization',
    'license': 'AGPL-3',
    'description': """
Plan contable genérico para la Argentina.

Incluye:
  - Wizard de configuración.
  - Plantilla del plan contable genérico.

""",
    'depends': [
        'l10n_multilang',
        'l10n_ar_invoice',
    ],
    'demo': [
    ],
    'test': [],
    'data': [
        'data/account_chart_respinsc.xml',
        'data/account_chart_monotrib.xml',
        # 'data/account_chart_coop.xml',
    ],
    'installable': False,
    'version': '9.0.0.0.0',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
