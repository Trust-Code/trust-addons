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
from lxml import etree
from xml import render


def send_request(obj_nfse, url, template, certificate):
    xml_send = render(obj_nfse, template)    
    print xml_send    
    
    #connection = HTTPSConnection('server', key_file='key_file', cert_file='cert_file')    
    #connection.request(u'POST', 'endereco', xml_send, {
    #        u'Content-Type': u'application/soap+xml; charset=utf-8',
    #        u'Content-Length': len(xml_send),
    #        })
    resposta = '<?xml version="1.0" encoding="utf-8"?>'\
        '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'\
        '<soap:Header>'\
        '<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl">'\
        '<cUF>42</cUF><versaoDados>2.00</versaoDados>'\
        '</nfeCabecMsg>'\
        '</soap:Header>'\
        '<soap:Body>'\
        '<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl">'\
        '<NFeResult>ok</NFeResult></nfeDadosMsg>'\
        '</soap:Body>'\
        '</soap:Envelope>' #connection.getresponse()   
    root = etree.fromstring(resposta)
    return root
    
