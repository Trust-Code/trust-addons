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
import re
import base64
import hashlib
from lxml import etree
from lxml import objectify
from datetime import datetime
from openerp import api, fields, models, tools

from openerp.addons.trust_base_nfse.service.xml import render
from openerp.addons.trust_base_nfse.service.signature import Assinatura
from openerp.addons.trust_base_nfse.service.signxml_test import assinar


class BaseNfse(models.TransientModel):
    _inherit = 'base.nfse'

    @api.multi
    def send_rps(self):
        if self.city_code == '6291':  # Campinas
            nfse = self._get_nfse_object()
            url = self._url_envio_nfse()

            client = self._get_client(url)
            path = os.path.dirname(os.path.dirname(__file__))
            xml_send = render(nfse, path, 'envio_rps.xml')

            xml_send = "<!DOCTYPE ns1:ReqEnvioLoteRPS [<!ATTLIST Lote Id ID #IMPLIED>]>" + \
                xml_send

            pfx_path = self._save_pfx_certificate()
            sign = Assinatura(pfx_path, self.password)
            xml_signed = sign.assina_xml(xml_send, '#lote:1ABCDZ')

            arq_temp = open('/home/danimar/Documentos/pyxmlsec.xml', 'w')
            arq_temp.write(xml_signed)
            arq_temp.close()

            xml_signed = xml_signed.replace("""<!DOCTYPE ns1:ReqEnvioLoteRPS [
<!ATTLIST Lote Id ID #IMPLIED>
]>""", "")

            response = client.service.testeEnviar(xml_signed)
            print response

        return super(BaseNfse, self).send_rps()

    @api.multi
    def cancel_nfse(self):
        if self.city_code == '6291':  # Campinas
            url = self._url_envio_nfse()
            client = self._get_client(url)

            # TODO Preencher corretamente
            obj_cancelamento = {
                'cancelamento': {
                    'nota_id': self.invoice_id.internal_number}}

            path = os.path.dirname(os.path.dirname(__file__))
            xml_send = render(
                path, 'cancelamento.xml', **obj_cancelamento)

            response = client.service.cancelar(xml_send)
            sent_xml = client.last_sent()
            received_xml = client.last_received()

            status = {'status': '', 'message': '', 'files': [
                {'name': '{0}-canc-envio.xml'.format(
                    obj_cancelamento['cancelamento']['nota_id']),
                 'data': base64.encodestring(sent_xml)},
                {'name': '{0}-canc-envio.xml'.format(
                    obj_cancelamento['cancelamento']['nota_id']),
                 'data': base64.encodestring(received_xml)}
            ]}
            if 'RetornoCancelamentoNFSe' in response:
                resp = objectify.fromstring(response)
                status['status'] = resp.Erros.Erro[0].Codigo
                status['message'] = resp.Erros.Erro[0].Descricao
                status['success'] = resp.Cabecalho.Sucesso
            else:
                status['status'] = '-1'
                status['message'] = response
                status['success'] = False

            return status

        return super(BaseNfse, self).cancel_nfse()

    @api.multi
    def check_nfse_by_rps(self):
        if self.city_code == '6291':  # Campinas

            url = self._url_envio_nfse()
            client = self._get_client(url)

            obj_check = {}  # TODO Preencher corretamente

            path = os.path.dirname(os.path.dirname(__file__))
            xml_send = render(obj_check, path, 'consulta_nfse_por_rps.xml')

            response = client.service.consultarNFSeRps(xml_send)
            print response  # TODO Tratar resposta

        return super(BaseNfse, self).check_nfse_by_rps()

    @api.multi
    def check_nfse_by_lote(self):
        if self.city_code == '6291':  # Campinas
            url = self._url_envio_nfse()
            client = self._get_client(url)

            obj_consulta = {}  # TODO Preencher corretamente

            path = os.path.dirname(os.path.dirname(__file__))
            xml_send = render(obj_consulta, path, 'consulta_lote.xml')

            response = client.service.consultarLote(xml_send)
            print response  # TODO Tratar resposta

        return super(BaseNfse, self).check_nfse_by_lote()

    @api.multi
    def print_pdf(self):
        if self.city_code == '6291':  # Campinas
            return self.env['report'].get_action(
                self, 'trust_nfse_campinas.danfse_report')

    def _url_envio_nfse(self):
        if self.city_code == '6291':  # Campinas
            return 'http://issdigital.campinas.sp.gov.br/WsNFe2/LoteRps.jws?wsdl'
        elif self.city_code == '5403':  # Uberlandia
            return 'http://udigital.uberlandia.mg.gov.br/WsNFe2/LoteRps.jws?wsdl'
        elif self.city_code == '0427':  # Belem-PA
            return 'http://www.issdigitalbel.com.br/WsNFe2/LoteRps.jws?wsdl'
        elif self.city_code == '9051':  # Campo Grande
            return 'http://issdigital.pmcg.ms.gov.br/WsNFe2/LoteRps.jws?wsdl'
        elif self.city_code == '5869':  # Nova Iguaçu
            return 'http://www.issmaisfacil.com.br/WsNFe2/LoteRps.jws?wsdl'
        elif self.city_code == '1219':  # Teresina
            return 'http://www.issdigitalthe.com.br/WsNFe2/LoteRps.jws?wsdl'
        elif self.city_code == '0921':  # São Luis
            return 'http://www.issdigitalslz.com.br/WsNFe2/LoteRps.jws?wsdl'
        elif self.city_code == '7145':  # Sorocaba
            return 'http://www.issdigitalsod.com.br/WsNFe2/LoteRps.jws?wsdl'

    def _get_nfse_object(self):
        if self.invoice_id:
            inv = self.invoice_id

            phone = inv.partner_id.phone or ''
            tomador = {
                'cpf_cnpj': re.sub('[^0-9]', '', inv.partner_id.cnpj_cpf or ''),
                'razao_social': inv.partner_id.legal_name or '',
                'logradouro': inv.partner_id.street or '',
                'numero': inv.partner_id.number or '',
                'complemento': inv.partner_id.street2 or '',
                'bairro': inv.partner_id.district or 'Sem Bairro',
                'cidade': '%s%s' % (inv.partner_id.state_id.ibge_code, inv.partner_id.l10n_br_city_id.ibge_code),
                'cidade_descricao': inv.company_id.partner_id.city or '',
                'uf': inv.partner_id.state_id.code,
                'cep': re.sub('[^0-9]', '', inv.partner_id.zip),
                'tipo_logradouro': 'Rua',
                'tipo_bairro': 'Normal',
                'ddd': re.sub('[^0-9]', '', phone.split(' ')[0]),
                'telefone': re.sub('[^0-9]', '', phone.split(' ')[1]),
                'inscricao_municipal': inv.partner_id.inscr_mun or '',
                'email': inv.partner_id.email or '',
            }

            phone = inv.partner_id.phone or ''
            prestador = {
                'cnpj': re.sub('[^0-9]', '', inv.company_id.partner_id.cnpj_cpf or ''),
                'razao_social': inv.company_id.partner_id.legal_name or '',
                'inscricao_municipal': inv.company_id.partner_id.inscr_mun or '',
                'cod_municipio': '%s%s' % (inv.company_id.partner_id.state_id.ibge_code, inv.company_id.partner_id.l10n_br_city_id.ibge_code),
                'cidade': inv.company_id.partner_id.city or '',
                'tipo_logradouro': 'Rua',
                'ddd': re.sub('[^0-9]', '', phone.split(' ')[0]),
                'telefone': re.sub('[^0-9]', '', phone.split(' ')[1]),
                'email': inv.company_id.partner_id.email or '',
            }

            deducoes = []

            itens = []
            for inv_line in inv.invoice_line:
                item = {
                    'descricao': inv_line.product_id.name[:80] or '',
                    'quantidade': str("%.4f" % inv_line.quantity),
                    'valor_unitario': str("%.4f" % (inv_line.price_unit)),
                    'valor_total': str("%.2f" % (inv_line.quantity * inv_line.price_unit)),
                }
                itens.append(item)

            valor_servico = inv.amount_total
            valor_deducao = 0.0

            data_envio = datetime.strptime(
                inv.date_in_out,
                tools.DEFAULT_SERVER_DATETIME_FORMAT)
            data_envio = data_envio.strftime('%Y%m%d')

            assinatura = '%011dNF   %012d%s%s %s%s%015d%015d%010d%014d' % \
                (int(prestador['inscricao_municipal']),
                 int(inv.internal_number),
                 data_envio, 'T', 'N', 'A',
                 valor_servico,
                 valor_deducao,
                 412040000,
                 int(tomador['cpf_cnpj']))

            assinatura = hashlib.sha1(assinatura).hexdigest()

            rps = [{
                'assinatura': assinatura,
                'tomador': tomador,
                'prestador': prestador,
                'serie': 'NF',  # inv.document_serie_id.code or '',
                'numero': inv.internal_number or '',
                'data_emissao': inv.date_in_out,
                'situacao': 'N',
                'serie_prestacao': '99',
                'codigo_atividade': '412040000',
                'aliquota_atividade': '5.00',
                'tipo_recolhimento': 'A',
                'municipio_prestacao': tomador['cidade'],
                'municipio_descricao_prestacao': tomador['cidade_descricao'],
                'operacao': 'A',
                'tributacao': 'T',
                'valor_pis': str("%.2f" % inv.pis_value),
                'valor_cofins': str("%.2f" % inv.cofins_value),
                'valor_csll': '0.00',
                'valor_inss': '0.00',
                'valor_ir': '0.00',
                'aliquota_pis': '0.00',
                'aliquota_cofins': '0.00',
                'aliquota_csll': '0.00',
                'aliquota_inss': '0.00',
                'aliquota_ir': '0.00',
                'deducoes': deducoes,
                'itens': itens,
            }]

            nfse_object = {
                'cidade': '6291',
                'cpf_cnpj': prestador['cnpj'],
                'remetente': prestador['razao_social'],
                'transacao': '',
                'data_inicio': datetime.now(),
                'data_fim': datetime.now(),
                'total_rps': '1',
                'total_servicos': str("%.2f" % inv.amount_total),
                'total_deducoes': '0.00',
                'lote_id': 'lote:1ABCDZ',
                'lista_rps': rps
            }
            return nfse_object
        return None
