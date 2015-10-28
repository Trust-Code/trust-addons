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

import base64
from lxml import etree
from ..service.nota_servico import NotaServico
from openerp import api, fields, models


class BaseNfse(models.Model):
    _name = 'base.nfse'

    city_code = fields.Char(u'Código Cidade', size=100)
    name = fields.Char('Nome', size=100)
    certificate = fields.Binary('Certificado')
    password = fields.Char('Senha', size=100)

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

            chave_temp = '/tmp/certificate'
            item.certificate
            arq_temp = open(chave_temp, 'w')
            arq_temp.write(base64.b64decode(item.certificate))
            arq_temp.close()

             
            nfse = item._get_nfse_object()
            url = item._url_envio_nfse()

            nota = NotaServico(key=item.password, certificate=chave_temp, 
                               city_code=3304557, environment="homologacao")
            
            response = nota.send_nfse(nfse, 'abrasf_rps.xml')        
            print response
            
    @api.multi
    def send_rps(self):
        pass
    
    @api.multi
    def cancel_nfse(self):
        pass        
        
    @api.multi
    def check_nfse_by_rps(self):
        pass
    
    def check_nfse_by_lote(self):
        pass
