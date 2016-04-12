# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
#              Danimar Ribeiro <danimaribeiro@gmail.com>                      #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################

import re
import logging
import requests

from openerp import models
from openerp.exceptions import Warning

_logger = logging.getLogger(__name__)


class L10nbrZip(models.Model):
    _inherit = 'l10n_br.zip'

    def _search_by_cep(self, zip_code):
        try:
            url_viacep = 'http://viacep.com.br/ws/' + \
                zip_code + '/json/unicode/'
            obj_viacep = requests.get(url_viacep)
            res = obj_viacep.json()
            if res:
                city = self.env['l10n_br_base.city'].search(
                    [('ibge_code', '=', res['ibge'][2:]),
                     ('state_id.code', '=', res['uf'])])

                self.env['l10n_br.zip'].create(
                    {'zip': re.sub('[^0-9]', '', res['cep']),
                     'street': res['logradouro'],
                     'district': res['bairro'],
                     'country_id': city.state_id.country_id.id,
                     'state_id': city.state_id.id,
                     'l10n_br_city_id': city.id})

        except Exception as e:
            _logger.error(e.message, exc_info=True)

    def _search_by_address(self, state_id, city_id, street):
        try:
            city = self.env['l10n_br_base.city'].browse(city_id)
            url_viacep = 'http://viacep.com.br/ws/' + city.state_id.code + \
                '/' + city.name + '/' + street + '/json/unicode/'
            obj_viacep = requests.get(url_viacep)
            results = obj_viacep.json()
            if results:
                for res in results:
                    city = self.env['l10n_br_base.city'].search(
                        [('ibge_code', '=', res['ibge'][2:]),
                         ('state_id.code', '=', res['uf'])])

                    self.env['l10n_br.zip'].create(
                        {'zip': re.sub('[^0-9]', '', res['cep']),
                         'street': res['logradouro'],
                         'district': res['bairro'],
                         'country_id': city.state_id.country_id.id,
                         'state_id': city.state_id.id,
                         'l10n_br_city_id': city.id})

        except Exception as e:
            _logger.error(e.message, exc_info=True)

    def zip_search_multi(self, country_id=False,
                         state_id=False, l10n_br_city_id=False,
                         district=False, street=False, zip_code=False):

        zip_ids = super(L10nbrZip, self).zip_search_multi(
            country_id=country_id,
            state_id=state_id, l10n_br_city_id=l10n_br_city_id,
            district=district, street=street, zip_code=zip_code)

        if len(zip_ids) == 0:
            if zip_code and len(zip_code) == 9:
                self._search_by_cep(zip_code)

            elif zip_code:
                raise Warning('Digite o cep corretamente')
            else:
                self._search_by_address(state_id, l10n_br_city_id, street)

            return super(L10nbrZip, self).zip_search_multi(
                country_id=country_id,
                state_id=state_id, l10n_br_city_id=l10n_br_city_id,
                district=district, street=street, zip_code=zip_code)
        else:
            return zip_ids

    def set_result(self, zip_obj=None):
        if zip_obj:
            zip_code = zip_obj.zip
            if len(zip_code) == 8:
                zip_code = '%s-%s' % (zip_code[0:5], zip_code[5:8])
            result = {
                'country_id': zip_obj.country_id.id,
                'state_id': zip_obj.state_id.id,
                'l10n_br_city_id': zip_obj.l10n_br_city_id.id,
                'district': zip_obj.district,
                'street': zip_obj.street or '',
                'zip': zip_code,
            }
        else:
            result = {}
        return result
