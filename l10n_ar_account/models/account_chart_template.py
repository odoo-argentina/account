# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api
import logging
_logger = logging.getLogger(__name__)


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    @api.model
    def _prepare_all_journals(
            self, acc_template_ref, company, journals_dict=None):
        """
        Inherit this function in order to add use document and other
        configuration if company use argentinian localization
        """
        journal_data = super(
            AccountChartTemplate, self)._prepare_all_journals(
            acc_template_ref, company, journals_dict)
        # if argentinian chart, we set use_argentinian_localization for company
        if company.localization == 'argentina':
            point_of_sale_type = self._context.get(
                'point_of_sale_type', 'manual')
            point_of_sale_number = self._context.get(
                'point_of_sale_number', 1)
            for vals_journal in journal_data:
                # for sale journals we use get_name_and_code function
                if vals_journal['type'] == 'sale':
                    name, code = self.env['account.journal'].get_name_and_code(
                        point_of_sale_type, point_of_sale_number)
                    vals_journal['name'] = name
                    vals_journal['code'] = code
                if vals_journal['type'] in [
                        'sale', 'purchase']:
                    vals_journal['point_of_sale_number'] = point_of_sale_number
                    vals_journal['point_of_sale_type'] = point_of_sale_type
        return journal_data

    # @api.model
    # def configure_chart(
    #         self, company_id, currency_id,
    #         chart_template_id, sale_tax_id, purchase_tax_id):
    #     # return True
    #     if self.env['account.account'].search(
    #             [('company_id', '=', company_id)]):
    #         _logger.warning(
    #             'There is already a chart of account for company_id %i' % (
    #                 company_id))
    #         return True
    #     _logger.info(
    #         'Configuring chart %i for company %i' % (
    #             chart_template_id, company_id))
    #     wizard = self.with_context(company_id=company_id).create({
    #         'company_id': company_id,
    #         'currency_id': currency_id,
    #         'only_one_chart_template': True,
    #         'chart_template_id': chart_template_id,
    #         'code_digits': 7,
    #         "sale_tax": sale_tax_id,
    #         "purchase_tax": purchase_tax_id,
    #         # 'sale_tax_rate': ,
    #         # 'purchase_tax_rate': ,
    #         # 'complete_tax_set': fie
    #         })
    #     wizard.execute()

    #     # add default tax to current products
    #     _logger.info('Updating products taxes')
    #     tax_vals = {}
    #     sale_tax_template = self.env['account.tax.template'].browse(
    #         sale_tax_id)
    #     sale_tax = self.env['account.tax'].search([
    #         ('company_id', '=', company_id),
    #         ('name', '=', sale_tax_template.name)], limit=1)
    #     if sale_tax:
    #         tax_vals['taxes_id'] = [(4, sale_tax.id)]

    #     purchase_tax_template = self.env['account.tax.template'].browse(
    #         purchase_tax_id)
    #     purchase_tax = self.env['account.tax'].search([
    #         ('company_id', '=', company_id),
    #         ('name', '=', purchase_tax_template.name)], limit=1)
    #     if purchase_tax:
    #         tax_vals['supplier_taxes_id'] = [(4, purchase_tax.id)]

    #     for product in self.env['product.product'].search([]):
    #         product.write(tax_vals)
    #     return True
