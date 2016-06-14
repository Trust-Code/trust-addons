# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2016 Trustcode - www.trustcode.com.br                         #
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


from openerp.addons.web import http
from openerp.addons.web.http import request


class LeadCapture(http.Controller):

    @http.route('/lead-capture', type='http', auth="public", cors="*")
    def lead_capture(self, **post):
        lead = {'name': 'Novo lead via API', 'type': 'lead'}
        request.env['crm.lead'].sudo().new_lead_via_api(lead, **post)
        request.cr.commit()
        return "true"


class HelpDeskApi(http.Controller):

    @http.route('/helpdesk/new', type='json', auth="none", cors="*")
    def new_solicitation(self, **kwargs):
        try:
            trustcode_id = request.env[
                'crm.helpdesk'].sudo().new_solicitation_api(**kwargs)
            request.cr.commit()
            return {'sucesso': True, 'trustcode_id': trustcode_id}
        except KeyError:
            return {'sucesso': False,
                    'erro': 'Instale o módulo helpdesk'}

    @http.route(
        '/helpdesk/interaction/new', type='json', auth="none", cors="*")
    def new_interaction(self, **kwargs):
        try:
            trustcode_id = request.env[
                'crm.helpdesk'].sudo().new_interaction(**kwargs)
            request.cr.commit()
            return {'sucesso': True, 'trustcode_id': trustcode_id}
        except KeyError:
            return {'sucesso': False,
                    'erro': 'Instale o módulo helpdesk'}

    @http.route(
        '/helpdesk/interaction/update', type='json', auth="public", cors="*")
    def update_interaction(self, **kwargs):
        try:
            trustcode_id = request.env[
                'crm.helpdesk'].sudo().update_interaction(**kwargs)
            request.cr.commit()
            return {'sucesso': True, 'trustcode_id': trustcode_id}
        except KeyError:
            return {'sucesso': False,
                    'erro': 'Instale o módulo helpdesk'}

    @http.route(
        '/helpdesk/list', type='json', auth="public", cors="*")
    def list_solicitation(self, **kwargs):
        try:
            solicitations = request.env[
                'crm.helpdesk'].sudo().list_solicitation(**kwargs)
            request.cr.commit()
            return {'sucesso': True, 'solicitations': solicitations}
        except KeyError:
            return {'sucesso': False,
                    'erro': 'Instale o módulo helpdesk'}
