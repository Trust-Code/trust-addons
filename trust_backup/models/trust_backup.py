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

from openerp import models, fields, api
from openerp.service.db import dump_db
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import socket
import os
import time
import zipfile
import oerplib
import logging
from datetime import datetime
from sys import exc_info

_logger = logging.getLogger(__name__)


def execute(connector, method, *args):
    res = False
    try:
        res = getattr(connector, method)(*args)
    except socket.error as e:
        raise e
    return res


class BackupExecuted(models.Model):
    _name = 'backup.executed'
    _order = 'backup_date'

    def _generate_s3_link(self):
        return self.s3_id

    configuration_id = fields.Many2one('opendb.backup', string="Configuração")
    backup_date = fields.Datetime(string="Data")
    s3_id = fields.Char(string="S3 Id")
    s3_url = fields.Char("Link S3", computed=_generate_s3_link)
    state = fields.Selection(
        string="Estado", default='not_started',
        selection=[('not_started', 'Não iniciado'),
                   ('executing',
                    'Executando'), ('sending', 'Enviando'),
                   ('error', 'Erro'), ('concluded', 'Concluído')])


class TrustBackup(models.Model):
    _name = 'trust.backup'

    @api.multi
    @api.depends('interval', 'licenca.display_name')
    def name_get(self):
        result = []
        for backup in self:
            result.append(
                (backup.id,
                 backup.licenca.display_name +
                 " - " +
                 backup.interval))
        return result

    host = fields.Char(string="Endereço", size=200, default='localhost')
    port = fields.Char(string="Porta", size=10, default='8069')
    interval = fields.Selection(
        string=u"Período",
        selection=[('hora', '1 hora'), ('seis', '6 horas'),
                   ('doze', '12 horas'), ('diario', u'Diário')])    

    send_to_s3 = fields.Boolean('Enviar Amazon S3 ?')
    backup_dir = fields.Char(string=u"Diretório", size=300)

    _defaults = {
        'backup_dir': lambda *a: os.getcwd() + '/auto_bkp/DBbackups',
        'host': lambda *a: 'localhost',
        'port': lambda *a: '8069'
    }

    @api.model
    def schedule_backup(self):
        oerp = oerplib.OERP(
            'localhost',
            protocol='xmlrpc',
            port=8069,
            timeout=1200)
        confs = self.search([])
        for rec in confs:
            db_list = oerp.db.list()
            database_name = rec.licenca.subdomain
            if database_name in db_list:
                try:
                    if not os.path.isdir(rec.backup_dir):
                        os.makedirs(rec.backup_dir)
                except:
                    raise
                bkp_file = '%s_%s.sql' % (
                    database_name, time.strftime('%Y%m%d_%H_%M_%S'))
                zip_file = '%s_%s.zip' % (
                    database_name, time.strftime('%Y%m%d_%H_%M_%S'))
                file_path = os.path.join(rec.backup_dir, bkp_file)
                zip_path = os.path.join(rec.backup_dir, zip_file)
                fp = open(file_path, 'wb')
                try:
                    dump_db(database_name, fp, backup_format='dump')
                except Exception as ex:
                    _logger.error(str(ex).decode('utf-8', 'ignore'),
                                  exc_info=True)
                    continue

                fp.close()
                with zipfile.ZipFile(zip_path, 'w') as zipped:
                    zipped.write(file_path)
                zipped.close()
                os.remove(file_path)

                backup_env = self.env['backup.executed']

                if rec.send_to_s3:
                    key = self.send_for_amazon_s3(zip_path, zip_file)
                    backup_env.create({'backup_date': datetime.now(),
                                       'configuration_id': rec.id,
                                       's3_id': key,
                                       'state': 'concluded'})
                else:
                    backup_env.create(
                        {'backup_date': datetime.now(),
                         'configuration_id': rec.id, 'state': 'concluded'})
            else:
                pass

    def send_for_amazon_s3(self, file_to_send, name_to_store):
        try:
            env_settings = self.env['server.config.settings']
            settings = env_settings.search_read(
                [], [
                    'aws_access_key', 'aws_secret_key'])
            if len(settings) > 0:
                access_key = settings[0]["aws_access_key"]
                secret_key = settings[0]["aws_secret_key"]

                conexao = S3Connection(access_key, secret_key)
                bucket = conexao.create_bucket('backups_pelican')

                k = Key(bucket)
                k.key = name_to_store
                k.set_contents_from_filename(file_to_send)
            else:
                _logger.error(
                    u'Configurações do Amazon S3 não setadas, \
                    pulando armazenamento de backup')
        except Exception as ex:
            _logger.error(str(ex).decode('utf-8', 'ignore'), exc_info=True)
