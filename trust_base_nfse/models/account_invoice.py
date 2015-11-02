# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2013  Danimar Ribeiro 26/06/2013                              #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

import os
import logging
import datetime
from openerp import api, fields, models
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    """account_invoice overwritten methods"""
    _inherit = 'account.invoice'

    state = fields.Selection(selection_add=[
        ('nfse_ready', u'Enviar NFS-e'),
        ('nfse_exception', u'Erro de autorização'),
        ('nfse_cancelled', 'Cancelada')])

    # def attach_file_event(self, cr, uid, ids, seq, att_type, ext, context):
    #    pass

    @api.multi
    def action_resend(self):
        print 'agora vai'
        self.state = 'nfse_ready'

    @api.multi
    def action_invoice_send_nfse(self):
        print 'chamou aqui'
        self.state = 'open'

    @api.multi
    def button_cancel(self):
        print 'passou aqui'
        return super(AccountInvoice, self).button_cancel()

    @api.multi
    def cancel_invoice_online(self):
        return 'ok'

    @api.multi
    def invoice_print(self):
        base_nfse = self.env['base.nfse'].create({'invoice_id': self.id,
                                                  'city_code': '6291'})

        return base_nfse.print_pdf()