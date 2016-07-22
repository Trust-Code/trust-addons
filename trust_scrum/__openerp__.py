# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Escalonador de Tarefas',
    'summary': """Distribui as tarefas não atribuidas pasra funcionarios\n
                  que estejam capacitados a lidar com elas, seguindo a ordem\n
                  de prioridade e então de criação. Atribui cores para as\n
                  tarefas baseado nos marcadores.""",
    'version': '1.0',
    'category': 'MRP',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': ['Mackilem Van der Laan Soares <mack.vdl@gmail.com>',
                     'Danimar Ribeiro <danimaribeiro@gmail.com>',
                     'Alessanandro Fernandes Martini \
                     <alessandrofmartini@gmail.com>'],
    'depends': ['hr', 'project'],
    'data': ['views/trust_scrum.xml',
             'wizard/escalonador_wizard.xml']
}
