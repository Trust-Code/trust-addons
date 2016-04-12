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


import os
import random
from werkzeug.wsgi import wrap_file
from werkzeug.wrappers import BaseResponse


from openerp import http
from openerp.http import request


class TrustBaseController(http.Controller):

    @http.route('/trust/logo', type='http', auth='none', methods=['GET'])
    def logo_login(self, **post):
        p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        number_rnd = random.randint(1, 15)
        p = os.path.join(p, 'static/src/img/fundo_{0}.jpg'.format(number_rnd))
        image = open(p, 'rb')
        return BaseResponse(wrap_file(request.httprequest.environ, image),
                            mimetype='image/png')
