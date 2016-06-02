# -*- coding: utf-8 -*-
{
    "name": "Argentina - Facturación y documentos AFIP",
    'version': '9.0.0.0.0',
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author':  'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'license': 'AGPL-3',
    'summary': '',
    'description': """
Argentina - Facturación y documentos AFIP
=========================================
Para actualizar el plan de cuentas de datos demo:
-------------------------------------------------
* borrar la parte de account.chart
* reemplazar ".template" por nada
* reemplazar <!-- <field name="company_id" ref=""/> --> por <field name="company_id" ref="company_ri"/>
* reemplazar <field name="chart_template_id" ref="ri_l10nAR_chart_template"/> por <!-- <field name="chart_template_id" ref="ri_l10nAR_chart_template"/> -->
""",
    'depends': [
          'account',
          'l10n_ar_base_vat',
          'partner_documents'
        ],
    'external_dependencies': {
    },
    'data': [
          'data/data_account_type.xml',
          'data/account_financial_report_data.xml',
          'data/responsability.xml',
          'data/afip_incoterm.xml',
          'data/afip_document_letter.xml',
          'data/afip.document_class.csv',
          'data/document_type.xml',
          'data/fiscal_position.xml',
          'data/res_country_cuit.xml',
          'data/res_country_afip_code.xml',
          'data/product_uom.xml',
          'data/res_partner.xml',
          'data/res_currency.xml',
          'data/account_payment_term.xml',
          # 'data/decimal_precision_data.xml', probando si no es necesario
          'wizard/account_journal_create_wizard_view.xml',
          'view/partner_view.xml',
          'view/company_view.xml',
          'view/country_view.xml',
          'view/afip_menuitem.xml',
          'view/product_uom_view.xml',
          'view/fiscal_position_view.xml',
          'view/afip_document_letter_view.xml',
          'view/afip_document_type_view.xml',
          'view/afip_responsability_view.xml',
          'view/afip_document_class_view.xml',
          'view/afip_point_of_sale_view.xml',
          'view/account_journal_afip_document_class_view.xml',
          'view/account_tax_code_view.xml',
          'view/tax_code_template_view.xml',
          'view/journal_view.xml',
          'view/invoice_view.xml',
          'view/account_move_view.xml',
          'view/account_move_line_view.xml',
          'view/currency_view.xml',
          'view/afip_incoterm_view.xml',
          'view/partner_bank_view.xml',
          'invoice_template.xml',
          'report/invoice_analysis.xml',
          'security/ir.model.access.csv',
          'security/l10n_ar_invoice_security.xml',
      ],
    'demo': [
          'demo/res_country_state_demo.xml',
          'demo/partner_demo.xml',
          'demo/company_demo.xml',
          # TODO tal vez sea mejor estos dos ejecutarlos con una accion ya que al hacer un init dan error porque ya existen movimientos
          'demo/fiscal_year_mono_demo.xml',
          'demo/fiscal_year_ri_demo.xml',
          'demo/account_chart_respinsc.xml',
          'demo/account_demo.xml',
          'demo/ri_purchase_invoice_demo.xml',
          'demo/ri_sale_invoice_demo.xml',
    ],
    'test': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
 }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
