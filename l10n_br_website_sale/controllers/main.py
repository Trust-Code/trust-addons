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
            val['email'] = data['email'] or False
            val['cnpj_cpf'] = data['cnpj_cpf'] or False
            val['number'] = data['number'] or False
            val['district'] = data['district'] or False
            val['street2'] = data['street2'] or False
            val['zip'] = data['zip'] or False
            if isinstance(data, dict):
                val['l10n_br_city_id'] = data['l10n_br_city_id'] or False
                val['country_id'] = data['country_id'] or False
                val['state_id'] = data['state_id'] or False
            else:
                val['l10n_br_city_id'] = data['l10n_br_city_id'].id or False
                val['country_id'] = data['country_id'].id or False
                val['state_id'] = data['state_id'].id or False
        if address_type == 'shipping':
            val['shipping_cnpj_cpf'] = data['cnpj_cpf'] or False
            val['shipping_number'] = data['number'] or False
            val['shipping_district'] = data['district'] or False
            val['shipping_street2'] = data['street2'] or False
            val['shipping_zip'] = data['zip'] or False
            if isinstance(data, dict):
                val['shipping_l10n_br_city_id'] = \
                    data['l10n_br_city_id'] or False
                val['shipping_country_id'] = data['country_id'] or False
                val['shipping_state_id'] = data['state_id'] or False
            else:
                val['shipping_l10n_br_city_id'] = \
                    data['l10n_br_city_id'].id or False
                val['shipping_country_id'] = data['country_id'].id or False
                val['shipping_state_id'] = data['state_id'].id or False
        return val

    def checkout_form_validate(self, data):
        error = super(L10nBrWebsiteSale, self).checkout_form_validate(data)
        if "cnpj_cpf" in data:
            cnpj_cpf = data["cnpj_cpf"]
            if cnpj_cpf and len(cnpj_cpf) == 18:
                if not validate_cnpj(cnpj_cpf):
                    error["cnpj_cpf"] = u"CNPJ inválido"
            elif cnpj_cpf and len(cnpj_cpf) == 14:
                if not validate_cpf(cnpj_cpf):
                    error["cnpj_cpf"] = u"CPF inválido"
            if cnpj_cpf:
                existe = request.env["res.partner"].sudo().search_count(
                    [('cnpj_cpf', '=', cnpj_cpf)])
                if existe > 0:
                    error["cnpj_cpf"] = u"CNPJ/CPF já cadastrado"
        return error
