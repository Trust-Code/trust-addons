# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
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


import requests
import suds
import suds.client
import suds_requests

from lxml import etree
from suds.sax.text import Raw
from certificate import converte_pfx_pem
from xml import render


class NotaServico(object):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.key = kwargs.pop("key")
        self.certificate = kwargs.pop("certificate")
        self.city_code = kwargs.pop("city_code")
        self.environment = kwargs.pop("environment")

    def _preparar_temp_pem(self):
        chave_temp = '/tmp/' + uuid4().hex
        certificado_temp = '/tmp/' + uuid4().hex

        chave, certificado = converte_pfx_pem(self.certificate, self.key)
        arq_temp = open(chave_temp, 'w')
        arq_temp.write(chave)
        arq_temp.close()

        arq_temp = open(certificado_temp, 'w')
        arq_temp.write(certificado)
        arq_temp.close()

        return chave_temp, certificado_temp

    def _get_client(self):
        cache_location = '/tmp/suds'
        cache = suds.cache.DocumentCache(location=cache_location)

        session = requests.Session()
        key, certificate = self._preparar_temp_pem()
        session.cert = (key, certificate)

        return suds.client.Client(
            self.base_url,
            cache=cache,
            transport=suds_requests.RequestsTransport(session)
        )

    def send_nfse(self, obj_nfse, template):
        client = self._get_client()
        xml_send = render(obj_nfse, template)
        # TODO O nome do método deve ser dinâmico
        response = client.service.GerarNfse(xml_send)
        return response

    def send_rps(self, obj_nfse, template):
        client = self._get_client()
        xml_send = render(obj_nfse, template)
        response = client.service.LoteRps(xml_send)
        return response

    def cancel_nfse(self, obj_nfse, template):
        client = self._get_client()
        xml_send = render(obj_nfse, template)
        response = client.service.CancelamentoNFSe(xml_send)
        return response
    
    def query_nfse(self, obj_nfse, template):
        client = self._get_client()
        xml_send = render(obj_nfse, template)
        response = client.service.ConsultaNFSe(xml_send)
        return response
