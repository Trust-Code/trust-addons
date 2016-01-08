
# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015 TrustCode - www.trustcode.com.br                         #
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


from openerp import api, fields, models


class MaterialAttributes(models.Model):
    _name = 'material.attributes'

    name = fields.Char('Nome', size=20)


class MaterialAttributesValue(models.Model):
    _name = 'material.attributes.value'

    name = fields.Char('Nome', size=20)
    value = fields.Char('Valor', size=50)
   
class MaterialAttributeLine(models.Model):
    _name = "material.attribute.line"
    _rec_name = 'attribute_id'

    product_tmpl_id = fields.Many2one(
        'product.template',
        'Product Template',
        required=True,
        ondelete='cascade')
    attribute_id = fields.Many2one(
        'material.attributes',
        'Attribute',
        required=True,
        ondelete='restrict')
    value_ids = fields.Many2many(
        'material.attributes.value',
        id1='line_id',
        id2='val_id',
        string='Product Attribute Value')
