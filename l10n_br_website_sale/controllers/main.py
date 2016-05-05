# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.http import request
import openerp.addons.website_sale.controllers.main as main


class L10nBrWebsiteSale(main.website_sale):

    @http.route(['/shop/get_cities'], type='json', auth="public",
                methods=['POST'], website=True)
    def get_cities_json(self, state_id):
        cities = request.env['l10n_br_base.city'].sudo().search(
            [('state_id', '=', int(state_id))])
        return [(city.id, city.name) for city in cities]

    def checkout_parse(self, address_type, data, remove_prefix=False):
        val = super(L10nBrWebsiteSale, self).checkout_parse(
            address_type, data, remove_prefix)
        if address_type == 'billing':
            val['cnpj_cpf'] = data['cnpj_cpf']
            val['number'] = data['number']
            val['district'] = data['district']
            val['street2'] = data['street2']
            val['zip'] = data['zip']
            val['l10n_br_city_id'] = data['l10n_br_city_id']
        return val

    def checkout_form_validate(self, data):
        error = super(L10nBrWebsiteSale, self).checkout_form_validate(data)
        if not data.get('cnpj_cpf'):
            error['cnpj_cpf'] = 'missing'
        if not data.get('number'):
            error['number'] = 'missing'
        if not data.get('district'):
            error['district'] = 'missing'
        if not data.get('street2'):
            error['street2'] = 'missing'
        if not data.get('zip'):
            error['zip'] = 'missing'
        if not data.get('l10n_br_city_id'):
            error['l10n_br_city_id'] = 'missing'
        return error
