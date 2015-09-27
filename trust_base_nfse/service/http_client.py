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


from httplib import HTTPSConnection
import ssl


class HttpClient(object):

    def __init__(self, url, chave_pem, certificado_pem):
        self.url = url
        self.chave_pem = chave_pem
        self.certificado_pem = certificado_pem

    def _headers(self):
        return {
            u'Content-type': u'application/soap+xml; charset=utf-8',
            u'Accept': u'application/soap+xml; charset=utf-8'
        }

    def post_xml(self, post, xml):
        # Python 2.7.9+ enable ssl certificate validation by default
        # We must disable because NF-e certificates are not trustable
        context = ssl._create_unverified_context()
        conexao = HTTPSConnection(self.url, '443', key_file=self.chave_pem,
                                  cert_file=self.certificado_pem, context=context)

        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            conexao.request(u'POST', post, xml, self._headers())
            response = conexao.getresponse()
            if response.status == 200:
                return response.read()
            return response.read()
        except Exception as e:
            print str(e)
        finally:
            conexao.close()
