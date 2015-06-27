# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-Trust-Code (<http://www.trustcode.com.br>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
try:
    import simplejson as json
except ImportError:
    import json
import logging
import pprint
import urllib2
import werkzeug

from openerp import http, SUPERUSER_ID
from openerp.http import request

_logger = logging.getLogger(__name__)


class CieloController(http.Controller):
    _return_url = '/cielo/retorno/'
    _notify_url = '/cielo/notificacao/'
    _status_url = '/cielo/status/'

    def cielo_validate_data(self, **post):
        pass

    @http.route('/cielo/retorno/', type='http', auth='none', methods=['POST'])
    def cielo_retorno(self, **post):
        """ Paypal IPN. """
        _logger.info('Beginning Paypal IPN form_feedback with post data %s', pprint.pformat(post))  # debug
        self.cielo_validate_data(**post)
        return ''

    @http.route('/cielo/notificacao/', type='http', auth="none", methods=['POST'])
    def cielo_notify(self, **post):
        """ Paypal DPN """
        _logger.info('Beginning Paypal DPN form_feedback with post data %s', pprint.pformat(post))  # debug
        self.cielo_validate_data(**post)
        return werkzeug.utils.redirect(return_url)

    @http.route('/cielo/status/', type='http', auth="none")
    def cielo_cancel(self, **post):
        """ When the user cancels its Paypal payment: GET on this route """
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        _logger.info('Beginning Paypal cancel with post data %s', pprint.pformat(post))  # debug
        return_url = self._get_return_url(**post)
        return werkzeug.utils.redirect(return_url)


