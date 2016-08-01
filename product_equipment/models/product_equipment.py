# -*- encoding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class TipoEquipamento(models.Model):
    _name = 'tipo.equipamento'

    name = fields.Char('Nome')
    group = fields.Selection([
        ('1', 'Computadores'),
        ('2', 'Servidores'),
        ('3', 'Dispositivos Móveis'),
        ('4', 'Acessórios'),
        ('5', 'Equipamentos de Rede'),
        ('6', 'Equipamentos de Telefonia'),
        ('7', 'Equipamentos de CFTV'),
        ('8', 'Outros')
        ],
        string='Grupo')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    partner_id = fields.Many2one('res.partner', string="Parceiro")

    group = fields.Selection([
        ('1', 'Computadores'),
        ('2', 'Servidores'),
        ('3', 'Dispositivos Móveis'),
        ('4', 'Acessórios'),
        ('5', 'Equipamentos de Rede'),
        ('6', 'Equipamentos de Telefonia'),
        ('7', 'Equipamentos de CFTV'),
        ('8', 'Outros')
        ],
        string='Grupo')

    equipment_id = fields.Many2one('tipo.equipamento', string="Equipamento")

    equipment_type = fields.Selection([
        ('1', 'Computador'),
        ('1', 'Notebook'),
        ('2', 'Servidor'),
        ('3', 'Smartphone'),
        ('3', 'Tablet'),
        ('4', 'Impressora'),
        ('4', 'Monitor'),
        ('5', 'Switch'),
        ('5', 'Roteador'),
        ],
        string='Tipo de Equipamento')

    tag_comp = fields.Integer(string="Etiqueta")
    customer_id = fields.Many2one('res.partner', string="Cliente")
    sector = fields.Char(max_length=30, string="Alocação")
    employee_id = fields.Many2one('res.users', string="Usuário de contato")
    access_code = fields.Char(max_length=30,
                              string="Código de Acesso (ammyy)")
    remote_access_password = fields.Char(max_length=30,
                                         string="Senha de Acesso Remoto")
    manufacturer = fields.Char(max_length=30, string="Fabricante")
    model = fields.Char(max_length=30, string="Modelo")
    serial_num = fields.Char(max_length=30, string="Número de Série")
    service_tag = fields.Char(max_length=30,
                              string="Etiqueta de Serviço (Dell)")
    buy_date = fields.Date(string="Data de Compra")
    guarantee_control = fields.Selection([
        ('yes', 'Sim'),
        ('no', 'Não'), ],
        string="Controla Garantia?")
    gurantee_period = fields.Char(max_length=30, string="Prazo de Garantia")
    processor = fields.Char(max_length=30, string="Processador")
    memory = fields.Char(max_length=30, string="Memória")
    hd = fields.Char(max_length=30, string="HD")
    motherboard_manufacturer = fields.Char(
        max_length=30, string="Fabricante e Modelo da Placa Mãe")
    equipment_name = fields.Char(max_length=30,
                                 string="Nome do Equipamento na Rede")
    web_type = fields.Selection([
        ('1', 'Grupo de Trabalho'),
        ('2', 'Domínio'), ],
        string="Tipo de Rede")
    web_name = fields.Char(max_length=30, string="Nome da Rede")
    user_local_login = fields.Char(
        max_length=30,
        string="Login usuário administrador local")
    user_local_password = fields.Char(
        max_length=30,
        string="Senha usuário administrador local")
    ip_type = fields.Selection([
        ('1', 'Fornecido po DHCP'),
        ('2', 'IP Fixo na Placa'), ],
        string="Tipo de endereço de IP")
    mac_address = fields.Char(max_length=30,
                              string="Endereço Físico (Mac Adress)")
    ip_address = fields.Char(max_length=30, string="Endereço IP (rede local)")
    sub_web_mask = fields.Char(max_length=30, string="Mascará sub-rede")
    gateway = fields.Char(max_length=30, string="Gateway")
    dns1 = fields.Char(max_length=30, string="DNS1")
    dns2 = fields.Char(max_length=30, string="DNS2")
    remote_access_door = fields.Char(
        max_length=30, string="Número de Porta de Acesso Remoto")
    server_print = fields.Selection([
        ('1', 'SIM'),
        ('2', 'NÃO'), ],
        string="Servidor de Impressão")
    printer_model = fields.Char(
        max_length=30, string="Marca/Modelo da Impressora Conectada")
    printer_path = fields.Char(
        max_length=30, string="Caminho na Rede para Acesso à Impressora")
    web_printer = fields.Char(
        max_length=30, string="Impressoras de Rede")
    routine_prog_user = fields.Char(
        max_length=30, string="Programas de Rotina do Computador/Usuário")
    email_bool = fields.Selection([
        ('1', 'SIM'),
        ('2', 'NÃO'), ],
        string="Usa E-mail?")
    email_use_type = fields.Selection([
        ('1', 'Webmail'),
        ('2', 'Outlook'),
        ('3', 'Outros'), ],
        string="Forma de Uso de E-mail")
    email_account = fields.Char(
        max_length=30, string="Conta de E-mail Cadastrada")
    email_password = fields.Char(
        max_length=30, string="Senha da Conta de E-mail")
    pop_server = fields.Char(
        max_length=30, string="Servidor Pop")
    smtp_server = fields.Char(
        max_length=30, string="Servidor SMTP")
    pop_door = fields.Char(
        max_length=30, string="Porta Pop")
    smtp_door = fields.Char(
        max_length=30, string="Porta SMTP")
    outlook_obs = fields.Text(
        string="Cadastramento de Conta Outlook")
    other_obs = fields.Text(
        string="Equipamento/Setor/Usuário")
    other_gen_info = fields.Text(
        string="Informações Gerais")
    op_system = fields.Char(max_length=30, string="Sistema Operacional")
    op_system_version = fields.Char(max_length=30,
                                    string="Versão do Sistema Operacional")
    antivirus = fields.Char(max_length=30, string="Antivírus")
    antivirus_version = fields.Char(max_length=30,
                                    string="Versão do Antivírus")
    tag_server = fields.Integer(string="Etiqueta")
    remote_acces_path_ts = fields.Char(max_length=30,
                                       string="Rota de Acesso Remoto via TS")
    ts_remote_access_door = fields.Integer(string="Porta de Acesso Remoto TS")
    service_tag_server = fields.Char(max_length=30,
                                     string="Etiqueta de Serviço (Dell)")
    server_function = fields.Char(max_length=50, string="Função do Servidor")
    admin_user_login = fields.Char(max_length=30,
                                   string="Login do Usuário Administrador")
    admin_user_password = fields.Char(max_length=30,
                                      string="Login do Usuário Administrador")
    other_info_and_obs = fields.Text(string="Outras Informações e Observações")
    tag_mobile = fields.Integer(string="Etiqueta")
    mobile_equipment_type = fields.Char(max_length=30,
                                        string="Tipo de Equipamento")
    tag_accessories = fields.Integer(string="Etiqueta")
    accessories_equipment_type = fields.Char(max_length=30,
                                             string="Tipo de Equipamento")
    tag_net_equipment = fields.Integer(string="Etiqueta")
    net_equipment_type = fields.Char(max_length=30,
                                     string="Tipo de Equipamento")
    tag_tel_equipment = fields.Integer(string="Etiqueta")
    tel_equipment_type = fields.Char(max_length=30,
                                     string="Tipo de Equipamento")
    tag_cftv_equipment = fields.Integer(string="Etiqueta")
    cftv_equipment_type = fields.Char(max_length=30,
                                      string="Tipo de Equipamento")
    tag_others = fields.Integer(string="Etiqueta")
    other_equipment_type = fields.Char(max_length=30,
                                       string="Tipo de Equipamento")
