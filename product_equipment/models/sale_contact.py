# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ClientTemplate(models.Model):
    _inherit = 'res.partner'

    web_name = fields.Char(max_length=30, string="Nome da Rede", required=True)
    web_type = fields.Selection([
        ('work', 'Grupo de Trabalho'),
        ('domain', 'Domínio'), ],
        string="Tipo de Rede",
        required=True)
    admin_user_login = fields.Char(max_length=30,
                                   string="Login Administrador do Domínio",
                                   required=True)
    admin_user_password = fields.Char(max_length=30,
                                      string="Senha Administrador do Domínio",
                                      required=True)
    wifi_name = fields.Char(max_length=30, string="Nome da Rede Wireless",
                            required=True)
    access_password = fields.Char(max_length=30, string="Senha de Acesso",
                                  required=True)
    dhcp_server = fields.Char(max_length=30, string="Servidor DHCP (Gateway)",
                              required=True)
    dns1_server = fields.Char(max_length=30, string="Servidor DNS1",
                              required=True)
    dns2_server = fields.Char(max_length=30, string="Servidor DNS2",
                              required=True)
    dhcp_controller = fields.Char(max_length=30,
                                  string="Equipamento Controlador do DHCP",
                                  required=True)
    net_provider_1 = fields.Char(max_length=30,
                                 string="Provedor de Internet 1 (Operadora)")
    broad_band_type_1 = fields.Char(max_length=30,
                                    string="Tipo de Banda Larga")
    net_speed_1 = fields.Char(max_length=30, string="Velocidade")
    ip_address_type_1 = fields.Char(max_length=30,
                                    string="Tipo de Endereço de IP")
    ip_address_1 = fields.Char(max_length=30, string="Endereço de IP")
    ddns_address_1 = fields.Char(max_length=30, string="Endereço DDNS")
    ddns_password_1 = fields.Char(max_length=30, string="Senha DDNS")
    net_provider_2 = fields.Char(max_length=30,
                                 string="Provedor de Internet 2 (Operadora)")
    broad_band_type_2 = fields.Char(max_length=30,
                                    string="Tipo de Banda Larga")
    net_speed_2 = fields.Char(max_length=30, string="Velocidade")
    ip_address_type_2 = fields.Char(max_length=30,
                                    string="Tipo de Endereço de IP")
    ip_address_2 = fields.Char(max_length=30, string="Endereço de IP")
    ddns_address_2 = fields.Char(max_length=30, string="Endereço DDNS")
    ddns_password_2 = fields.Char(max_length=30, string="Senha DDNS")
    email_host_prov = fields.Char(max_length=30,
                                  string="Provedor de Hospedagem e E-mails")
    login = fields.Char(max_length=30, string="Login")
    password = fields.Char(max_length=30, string="Password")
    other_host_info = fields.Text(string="Outras Informações de Hospedagem")
    sys_util_partner = fields.Text(string="Sistemas Utilizados pelo Cliente")
    other_gen_info = fields.Text(string="Outras Informações Gerais")
