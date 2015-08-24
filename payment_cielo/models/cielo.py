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

import re
from openerp import models, fields, SUPERUSER_ID


class AcquirerCielo(models.Model):
    _inherit = 'payment.acquirer'

    def _get_cielo_urls(self, cr, uid, environment, context=None):
        """ Cielo URLS """
        return {
            'cielo_form_url':
                'https://cieloecommerce.cielo.com.br/Transactional/Order/Index'
        }

    def _get_providers(self, cr, uid, context=None):
        providers = super(AcquirerCielo, self)._get_providers(
            cr, uid, context=context)
        providers.append(['cielo', 'Cielo'])
        return providers

    cielo_merchant_id = fields.Char(
        string='Cielo Merchant ID',
        help='''The Merchant ID is used to ensure communications
            coming from Paypal are valid and secured.''')

    def form_preprocess_values(self, cr, uid, id, reference, amount,
                               currency_id, tx_id, partner_id,
                               partner_values, tx_values, context=None):
        partner_values, tx_values = super(
            AcquirerCielo,
            self).form_preprocess_values(
            cr,
            uid,
            id,
            reference,
            amount,
            currency_id,
            tx_id,
            partner_id,
            partner_values,
            tx_values,
            context)

        parceiro = self.pool['res.partner'].browse(cr, uid, partner_id)
        partner_values.update({
            'cpf': parceiro.cnpj_cpf or '',
        })
        pedido_ids = self.pool['sale.order'].search(
            cr, uid, [('name', '=', reference),
                      ('partner_id', '=', partner_id)])
        pedido = self.pool['sale.order'].browse(cr, uid, pedido_ids[0])
        entrega = pedido.partner_shipping_id

        partner_values.update({
            'zip': entrega.zip, 'street': entrega.street,
            'number': entrega.number, 'district': entrega.district,
            'complement': entrega.street2,
            'city': entrega.l10n_br_city_id.name, 'state': entrega.state_id
        })
        lines = []

        for line in pedido.order_line:
            lines.append({
                'name': re.sub(
                    '[^a-zA-z0-9 ]', '',
                    line.name[:80]).replace('[', '').replace(']', ''),
                'price': '{:.0f}'.format(line.price_unit * 100),
                'quantity': '{:.0f}'.format(line.product_uom_qty),
                'zip': re.sub('[^0-9]', '', entrega.zip),
                'index': str(len(lines) + 1)})

        tx_values.update({'sale_lines': lines})

        return partner_values, tx_values

    def cielo_form_generate_values(
            self, cr, uid, id, partner_values, tx_values, context=None):
        self.pool['ir.config_parameter'].get_param(
            cr,
            SUPERUSER_ID,
            'web.base.url')
        acquirer = self.browse(cr, uid, id, context=context)

        cielo_tx_values = dict(tx_values)
        cielo_tx_values.update({
            'merchant_id': acquirer.cielo_merchant_id,
            'order_id': tx_values['reference'],
            'shipping_type': '2',

            'zip_code': re.sub('[^0-9]', '', partner_values['zip'] or '-'),
            'street': partner_values.get('street', ''),
            'street_number': partner_values.get('number', ''),
            'complement': partner_values.get('complement', ''),
            'district': partner_values.get('district', ''),
            'city': partner_values.get('city', ''),
            'state': partner_values['state'].code or '',

            'sale_lines': tx_values['sale_lines'],

            'partner_name': partner_values.get('name', ''),
            'partner_email': partner_values.get('email', ''),
            'partner_cpf': re.sub('[^0-9]', '',
                                  partner_values.get('cpf', '-')),
            'partner_phone': re.sub('[^0-9]', '',
                                    partner_values.get('phone', '-')),
        })
        if acquirer.fees_active:
            cielo_tx_values['handling'] = '%.2f' % cielo_tx_values.pop(
                'fees',
                0.0)

        return partner_values, cielo_tx_values

    def cielo_get_form_action_url(self, cr, uid, id, context=None):
        acquirer = self.browse(cr, uid, id, context=context)
        return self._get_cielo_urls(
            cr, uid, acquirer.environment, context=context)['cielo_form_url']


class TransactionCielo(models.Model):
    _inherit = 'payment.transaction'

    cielo_transaction_id = fields.Char(string='Transaction ID')
    transaction_type = fields.Char(string='Transaction type')
