# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Multi Images in Website',
    'summary': """Implement multi images to shop in products""",
    'version': '8.0.1.0.0',
    'category': 'website',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>'
    ],
    'depends': [
        'base_multi_image', 'product_multi_image',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_templates.xml',
    ],
}
