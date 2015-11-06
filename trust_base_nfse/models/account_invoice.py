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
import base64
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

    def _attach_files(self, obj_id, model, data, filename):
        obj_attachment = self.env['ir.attachment']

        obj_attachment.create({
            'name': filename,
            'datas': base64.b64encode(data),
            'datas_fname': filename,
            'description': '' or _('No Description'),
            'res_model': model,
            'res_id': obj_id,
        })

    @api.multi
    def action_resend(self):
        self.state = 'nfse_ready'

    @api.multi
    def action_invoice_send_nfse(self):
        event_obj = self.env['l10n_br_account.document_event']
        base_nfse = self.env['base.nfse'].create({'invoice_id': self.id,
                                                  'city_code': '6291'})

        send = base_nfse.send_rps()
        vals = {
            'type': 'Envio NFS-e',
            'status': send['status'],
            'company_id': self.company_id.id,
            'origin': '[NFS-e] {0}'.format(self.internal_number),
            'message': send['message'],
            'state': 'done',
            'document_event_ids': self.id
        }
        event = event_obj.create(vals)
        for xml_file in send['files']:
            self._attach_files(event.id, 'l10n_br_account.document_event',
                               xml_file['data'], xml_file['name'])

        if send['success']:
            self.state = 'open'
        else:
            self.state = 'nfse_exception'

    @api.multi
    def button_cancel(self):
        cancel_result = self.cancel_invoice_online()
        if cancel_result:
            return super(AccountInvoice, self).button_cancel()

    @api.multi
    def cancel_invoice_online(self):
        event_obj = self.env['l10n_br_account.document_event']
        base_nfse = self.env['base.nfse'].create({'invoice_id': self.id,
                                                  'city_code': '6291'})

        cancelamento = base_nfse.cancel_nfse()
        vals = {
            'type': 'Cancelamento NFS-e',
            'status': cancelamento['status'],
            'company_id': self.company_id.id,
            'origin': '[NFS-e] {0}'.format(self.internal_number),
            'message': cancelamento['message'],
            'state': 'done',
            'document_event_ids': self.id
        }
        event = event_obj.create(vals)
        for xml_file in cancelamento['files']:
            self._attach_files(event.id, 'l10n_br_account.document_event',
                               xml_file['data'], xml_file['name'])
        return cancelamento['success']

    @api.multi
    def invoice_print(self):
        base_nfse = self.env['base.nfse'].create({'invoice_id': self.id,
                                                  'city_code': '6291'})

        return base_nfse.print_pdf()
