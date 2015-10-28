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

from reportlab.platypus.tables import Table
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib import colors
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import ParagraphStyle

inch = 28.34


class Rps(object):

    objeto = None

    def __init__(self, objetoNFe):
        self.objeto = objetoNFe

    def _header(self):
        data = [
            ['Recebemos de verdesaine industria e comércio os produtos constantes na nota fiscal abaixo ', '',
             'NF-e\nNº 000.000.001\nSérie 001'],
            ['Data de recebimento',
             'Identificação e assinatura do recebedor',
             '']
        ]

        estilo = [('SPAN', (0, 0), (1, 0)),
                  ('SPAN', (2, 0), (2, 1)),
                  ('FONTSIZE', (0, 0), (1, 1), 7.0),
                  ('VALIGN', (0, 0), (1, 1), 'TOP'),
                  ('ALIGN', (2, 0), (2, 1), 'CENTER'),
                  ('TOPPADING', (0, 0), (1, 1), 6),
                  ('GRID', (0, 0), (3, 1), 0.5, colors.black)]
        colunas = [4 * inch, 12 * inch, 4 * inch]
        linhas = [20, 30]
        table = Table(data, style=estilo, colWidths=colunas, rowHeights=linhas)
        return table

    def _field(self, label, value):
        estilo = ParagraphStyle('default')
        return Paragraph(
            '<font size="8">' + label + '</font>' + '<br />' + value, estilo)

    def _segundo_cabecalho(self):
        data = [
            [self._field('Natureza da operação', 'Venda de produção do estabelecimento'), '',
             self._field('Protocolo de autorização de uso', '12345678956665487')],
            [self._field('Inscrição estadual', '156466487897'),
             self._field(
                'Inscrição estadual substituto tributário',
                '1456465456'),
                self._field('CNPJ', '87.224.633/0001-61'), ]
        ]

        estilo = [('SPAN', (0, 0), (1, 0)),
                  ('FONTSIZE', (0, 0), (1, 1), 7.0),
                  ('GRID', (0, 0), (2, 1), 0.5, colors.black)]
        colunas = [6 * inch, 7 * inch, 7 * inch]
        table = Table(data, style=estilo, colWidths=colunas)
        return table

    def generate(self):
        doc = SimpleDocTemplate(
            '/home/danimar/projetos/pdfs/danfe.pdf',
            pagesize=A4, leftMargin=0.5 * inch, rightMargin=0.5 * inch,
            topMargin=0.5 * inch, bottomMargin=0.5 * inch)

        elementos = []

        elementos.append(self._header())
        elementos.append(self._segundo_cabecalho())

        doc.build(elementos)
