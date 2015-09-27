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

import os
from lxml import etree
from xml import render

from uuid import uuid4
from .certificate import converte_pfx_pem
from .http_client import HttpClient
from .signature import Assinatura


class Comunicacao(object):
    url = ''
    web_service = ''
    metodo = ''
    tag_retorno = ''

    def __init__(self, certificado, senha):
        self.certificado = certificado
        self.senha = senha

    def _preparar_temp_pem(self):
        chave_temp = '/tmp/' + uuid4().hex
        certificado_temp = '/tmp/' + uuid4().hex

        chave, certificado = converte_pfx_pem(self.certificado, self.senha)
        arq_temp = open(chave_temp, 'w')
        arq_temp.write(chave)
        arq_temp.close()

        arq_temp = open(certificado_temp, 'w')
        arq_temp.write(certificado)
        arq_temp.close()

        return chave_temp, certificado_temp

    def _validar_dados(self):
        assert self.url != '', "Url servidor não configurada"
        assert self.web_service != '', "Web service não especificado"
        assert self.certificado != '', "Certificado não configurado"
        assert self.senha != '', "Senha não configurada"
        assert self.metodo != '', "Método não configurado"
        assert self.tag_retorno != '', "Tag de retorno não configurado"

    def send_request(self, obj_nfse, url, template):
        xml_send = render(obj_nfse, template)
        # self._validar_dados()

        assinatura = Assinatura(self.certificado, '123456')
        xml_signed = assinatura.assina_xml(xml_send, '#123')
        print xml_signed

        chave, certificado = self._preparar_temp_pem()
        client = HttpClient(self.url, chave, certificado)
        xml_retorno = client.post_xml(self.web_service, xml_signed)

        return etree.fromstring(xml_retorno)
