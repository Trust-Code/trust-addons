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

from lxml import etree
from ..service.webservice import send_request
from openerp import api, fields, models


class BaseNfse(models.Model):
    _name = 'base.nfse'

    name = fields.Char('Nome', size=100)

    def _url_envio_rps(self):
        return ''

    def _url_envio_nfse(self):
        return ''

    def _url_cancelamento_nfse(self):
        return ''

    def _url_consulta_lote_rps(self):
        return ''

    def _url_consulta_nfse_por_rps(self):
        return ''

    def _get_nfse_object(self):
        """
        Sobrescrever este método para adicionar novos itens ao gerar o xml.
        Returns:
            dict: retorna um dicionário com os dados da nfse
         """
        tomador = {'cnpj': '8768532.234', 'razao_social': 'MILTON LOPES', 'endereco': 'Rua das Flores',
                   'numero': 123, 'complemento': '1358', 'bairro': u'São Lourenço', 'cod_municipio': '4214805',
                   'uf': 'SC', 'cep': '88032050'}
        prestador = {'cnpj': '12154126', 'inscricao_municipal': '1234'}

        rps = [{'tomador': tomador,
                'prestador': prestador},

               {'tomador': tomador,
                'prestador': prestador}]

        nfse_object = {
            'id': '123',
            'cnpj': '989788.98/3233',
            'numero_lote': '123',
            'lista_rps': rps
        }
        return nfse_object

    def _get_nfse_return_object(self, xml_root):
        result = {}

        find = etree.XPath("/a:Envelope/a:Header/b:nfeCabecMsg/b:cUF/text()",
                           namespaces={'a': 'http://www.w3.org/2003/05/soap-envelope',
                                       'b': 'http://www.portalfiscal.inf.br/nfe/wsdl'})
        print find(xml_root)[0]

        return result

    def _validate_result(self, result):
        pass

    @api.multi
    def generate_nfse(self):
        for item in self:
            nfse = item._get_nfse_object()
            url = item._url_envio_nfse()
            xml_root = send_request(nfse, url, 'abrasf_rps.xml', None)
            resposta = item._get_nfse_return_object(xml_root)
            print resposta
            item._validate_result(resposta)

    @api.multi
    def cancel_nfse(self):
        pass

    @api.multi
    def check_nfse(self):
        pass
