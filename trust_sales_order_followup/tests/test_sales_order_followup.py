# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
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
###############################################################################

import time
from openerp.tests import common
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class Test_SalesOrderFollowUp(common.TransactionCase):

    def setUp(self):
        super(Test_SalesOrderFollowUp, self).setUp()
        self.partner = self.env['res.partner'].create(
            {'name': 'Danimar Ribeiro'})
        self.order = self.env['sale.order'].create(
            {'partner_id': self.partner.id})

    def test_action_create_meeting(self):
        res = self.order.action_create_meeting()

        self.assertEqual(res['context']['default_partner_id'], self.partner.id)
        self.assertEqual(res['res_model'], u'calendar.event')
        self.assertEqual(res['type'], u'ir.actions.act_window')

    def test_record_count(self):
        self.env['calendar.event'].create(
            {'name': 'Evento', 'sale_order_id': self.order.id,
             'start_datetime': time.strftime(DEFAULT_SERVER_DATE_FORMAT),
             'stop_datetime': time.strftime(DEFAULT_SERVER_DATE_FORMAT)}
        )

        self.assertEqual(self.order.meeting_count, 1,
                         u"Numero de reunioes para o pedido invalido")
