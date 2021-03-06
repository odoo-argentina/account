# -*- coding: utf-8 -*-
{
    "name": "Argentina - Facturación y documentos AFIP",
    'version': '9.0.0.0.0',
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'ADHOC SA,Moldeo Interactive',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'account_document',
        'l10n_ar_partner',
    ],
    'external_dependencies': {
    },
    'data': [
        'data/afip_responsible_type.xml',
        'data/account_document_letter.xml',
        'data/account.document.type.csv',
        'data/afip_incoterm.xml',
        'data/res_country_afip_code.xml',
        'data/res_country_cuit.xml',
        'data/product_uom.xml',
        'data/res_currency.xml',
        'data/res_partner.xml',
        'data/account_tax_group.xml',
        # TODO analizar y migrar
        # 'data/account_financial_report_data.xml',
        # 'data/account_payment_term.xml',
        'view/res_partner_view.xml',
        'view/res_company_view.xml',
        'view/afip_menuitem.xml',
        'view/afip_incoterm_view.xml',
        'view/res_country_view.xml',
        'view/res_currency_view.xml',
        'view/account_fiscal_position_view.xml',
        'view/product_uom_view.xml',
        'view/account_journal_view.xml',
        'view/account_invoice_view.xml',
        'view/afip_responsability_type_view.xml',
        'view/account_document_letter_view.xml',
        'view/account_document_type_view.xml',
        'res_config_view.xml',
        # TODO migrar
        # 'report/invoice_analysis.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/partner_demo.xml',
        'demo/company_demo.xml',
    ],
    'test': [
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
