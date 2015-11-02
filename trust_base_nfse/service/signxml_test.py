'''
Created on 2 de nov de 2015

@author: danimar
'''

import base64
from cStringIO import StringIO
from lxml.etree import ElementTree
from signxml import xmldsig, methods
from .certificate import converte_pfx_pem
from OpenSSL.crypto import *


def assinar(xml, pfx, senha):
    p12 = load_pkcs12(file(pfx, 'rb').read(), '123')

    cert = p12.get_certificate()
    key = p12.get_privatekey()

    cert, key = converte_pfx_pem(pfx, str(senha))
    root = ElementTree.fromstring(xml)
    signed_root = xmldsig(root).sign(
        key=key,
        cert=cert,
        reference_uri='#lote:1ABCDZ',
        method=methods.detached)
    print signed_root
