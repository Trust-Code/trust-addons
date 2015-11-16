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


from openerp import api, models


class ResUser(models.Model):
    _inherit = 'res.users'

    def authenticate(self, db, login, password, user_agent_env):
        result = super(ResUser, self).authenticate(db, login, password,
                                                   user_agent_env)

        if result:
            cr = self.pool.cursor()
            try:
                employee = self.pool['hr.employee'].browse(cr, result, result)
                if employee.state == 'absent':
                    employee.attendance_action_change()
                cr.commit()
            finally:
                cr.close()
        return result

    @api.model
    def logout_user(self):
        employee = self.env['hr.employee'].browse(self.env.user.id)
        if employee.state == 'present':
            employee.attendance_action_change()
        return True
