# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner_Wkf',
    'summary': "Cria um wdget de estados que confirma as\
                infomações do cliente.",
    'version': '8.0.1.0.0',
    'category': 'Website',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Alessandro Fernandes Martini <alessandrofmartini@gmail.com>',
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
    ],
    'depends': [
        'l10n_br_base',
        'account',
        'web_fields_masks'
    ],
    'data': ['views/res_partner.xml',
             ],
}
