# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Exportação XML NFS-e - Florianópolis',
    'summary': """Realiza a exportação em xml das notas fiscais de serviço""",
    'version': '8.0.1.0.0',
    'category': 'Website',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>'
    ],
    'depends': [
        'l10n_br_account_service', 'l10n_br_account_withholding'
    ],
    'data': [
        'views/res_company.xml',
        'wizard/nfse_florianopolis_export_view.xml',
    ],
}
