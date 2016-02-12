# -*- coding: utf-8 -*-
{
    'name': 'Argentina - Planes Contables',
    'author': 'Moldeo Interactive,ADHOC SA',
    'category': 'Localization/Account Charts',
    'license': 'AGPL-3',
    'depends': [
        'l10n_multilang',
    ],
    'test': [],
    'data': [
        'data/account_chart_template.xml',
        'data/account_chart_respinsc.xml',
        'data/account_tax_template.xml',
        'data/account_fiscal_template.xml',
        'account_chart_template.yml',
        'data/menuitem.xml',
        # TODO include
        # 'data/account_chart_monotrib.xml',
        # 'data/account_chart_coop.xml',
        # 'data/account_chart_agro.xml',
    ],
    'demo': [
        'demo/l10n_be_demo.yml',
        '../account/demo/account_bank_statement.yml',
        '../account/demo/account_invoice_demo.yml',
    ],
    'installable': False,
    'version': '9.0.0.0.0',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
