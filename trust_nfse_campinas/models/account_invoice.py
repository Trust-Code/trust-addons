# -*- coding: utf-8 -*-
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


from openerp import api, fields, models

FIELD_STATE = {'draft': [('readonly', False)]}


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    operation = fields.Selection([('A', u"Sem Dedução"),
                                  ('B', u"Com dedução/Materiais"),
                                  ('C', u"Imune/Isenta de ISSQN"),
                                  ('D', u"Devolução/Simples Remessa"),
                                  ('J', u"Intermediação")], u"Operação",
                                 default='A', readonly=True,
                                 states=FIELD_STATE)

    taxation = fields.Selection([('C', u"Isenta de ISS"),
                                 ('E', u"Não incidência no município"),
                                 ('F', u"Imune"),
                                 ('K', u"Exigibilidd Susp.Dec.J/Proc.A"),
                                 ('N', u"Não Tributável"),
                                 ('T', u"Tributável"),
                                 ('G', u"Tributável Fixo"),
                                 ('H', u"Tributável S.N."),
                                 ('M', u"Micro Empreendedor Individual(MEI)")],
                                u"Tributação", default='T',
                                readonly=True, states=FIELD_STATE)

    cnae_id = fields.Many2one('l10n_br_account.cnae', string=u"CNAE",
                              readonly=True, states=FIELD_STATE)
    lote_nfse = fields.Char(u'Lote', size=20, readonly=True, states=FIELD_STATE)
    transaction = fields.Char(u'Transação', size=60,
                              readonly=True, states=FIELD_STATE)
