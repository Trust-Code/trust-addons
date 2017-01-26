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

from . import controllers

import pytz

from openerp.fields import Datetime
from openerp.tools import ustr


def convert_to_export(self, value, env):
    """Monkeypatch para converter timezone de UTC para a do cliente"""
    if not value:
        return ''
    br_timezone = pytz.timezone(env.context.get('tz', u'America/Sao_Paulo'))
    datetime_as_utc = pytz.utc.localize(self.from_string(value), is_dst=None)
    datetime_as_br = datetime_as_utc.astimezone(br_timezone)
    value = self.to_string(datetime_as_br)
    return self.from_string(value) if env.context.get('export_raw_data') \
        else ustr(value)


Datetime.convert_to_export = convert_to_export
