# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 Trustcode - www.trustcode.com.br                         #
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


import simplejson
from werkzeug import url_decode
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from werkzeug.datastructures import Headers

from openerp.tools import html_escape
from openerp.tools.safe_eval import safe_eval
from openerp.addons.web.http import route, request
from openerp.addons.web.controllers.main import _serialize_exception
from openerp.addons.report.controllers.main import ReportController


class TrustReportController(ReportController):

    @route()
    def report_download(self, data, token):
        """This function is used by 'qwebactionmanager.js' in order to trigger
        the download of  a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report
        internal url ([0]) and type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = simplejson.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type == 'qweb-pdf':
                reportname = url.split('/report/pdf/')[1].split('?')[0]

                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')

                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids,
                                                  converter='pdf')
                else:
                    # Particular report:
                    # decoding the args represented in JSON
                    data = url_decode(url.split('?')[1]).items()
                    response = self.report_routes(
                        reportname, converter='pdf', **dict(data))

                filename = None
                if docids:
                    cr, uid = request.cr, request.uid
                    report = request.registry['report']._get_report_from_name(
                        cr, uid, reportname)
                    if report.attachment:
                        obj = request.registry[report.model].browse(
                            cr, uid, int(docids))
                        filename = safe_eval(
                            report.attachment, {'object': obj})
                    else:
                        filename = (report.name or reportname) + '.pdf'

                if not filename:
                    filename = reportname + '.pdf'
                filename = '"%s"' % filename
                response.headers.add(
                    'Content-Disposition',
                    'attachment; filename=%s;' %
                    filename)
                response.set_cookie('fileToken', token)
                return response
            elif type == 'controller':
                reqheaders = Headers(request.httprequest.headers)
                response = Client(
                    request.httprequest.app,
                    BaseResponse).get(
                    url,
                    headers=reqheaders,
                    follow_redirects=True)
                response.set_cookie('fileToken', token)
                return response
            else:
                return
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(simplejson.dumps(error)))
