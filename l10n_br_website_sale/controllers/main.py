# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.http import request
import openerp.addons.website_sale.controllers.main as main
from openerp.addons.l10n_br_base.tools.fiscal import (
    validate_cnpj,
    validate_cpf
)


class L10nBrWebsiteSale(main.website_sale):

    mandatory_billing_fields = ["name", "phone", "email", "cnpj_cpf", "zip",
                                "street", "number", "district", "country_id",
                                "state_id", "l10n_br_city_id"]
    mandatory_shipping_fields = ["name", "phone", "zip",
                                 "street", "number", "district", "country_id",
                                 "state_id", "l10n_br_city_id"]

    @http.route(['/shop/get_cities'], type='json', auth="public",
                methods=['POST'], website=True)
    def get_cities_json(self, state_id):
        if state_id.isdigit():
            cities = request.env['l10n_br_base.city'].sudo().search(
                [('state_id', '=', int(state_id))])
            return [(city.id, city.name) for city in cities]
        return []

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
        if address_type == 'shipping':
            val['shipping_cnpj_cpf'] = data['cnpj_cpf']
            val['shipping_number'] = data['number']
            val['shipping_district'] = data['district']
            val['shipping_street2'] = data['street2']
            val['shipping_zip'] = data['zip']
            val['shipping_l10n_br_city_id'] = data['l10n_br_city_id']
        return val

    def checkout_form_validate(self, data):
        error = super(L10nBrWebsiteSale, self).checkout_form_validate(data)
        if "cnpj_cpf" in data:
            cnpj_cpf = data["cnpj_cpf"]
            if len(cnpj_cpf) == 18:
                if not validate_cnpj(cnpj_cpf):
                    error["cnpj_cpf"] = u"CNPJ inválido"
            elif len(cnpj_cpf) == 14:
                if not validate_cpf(cnpj_cpf):
                    error["cnpj_cpf"] = u"CPF inválido"
            else:
                error["cnpj_cpf"] = u"CNPJ/CPF inválido"
            existe = request.env["res.partner"].sudo().search_count(
                [('cnpj_cpf', '=', cnpj_cpf)])
            if existe > 0:
                error["cnpj_cpf"] = u"CNPJ/CPF já cadastrado"
        return error
