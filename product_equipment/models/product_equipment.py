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
        string='Grupo',
        required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

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
        string='Grupo',
        required=True)

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
        string='Tipo de Equipamento',
        required=True)

    tag_comp = fields.Integer(string="Etiqueta", required=True)
    customer_id = fields.Many2one('res.partner', string="Cliente",
                                  required=True)
    sector = fields.Char(max_length=30, string="Alocação", required=True)
    employee_id = fields.Many2one('res.users', string="Usuário de contato",
                                  required=True)
    access_code = fields.Char(max_length=30,
                              string="Código de Acesso (ammyy)",
                              required=True)
    remote_access_password = fields.Char(max_length=30,
                                         string="Senha de Acesso Remoto",
                                         required=True)
    manufacturer = fields.Char(max_length=30, string="Fabricante",
                               required=True)
    model = fields.Char(max_length=30, string="Modelo", required=True)
    serial_num = fields.Char(max_length=30, string="Número de Série",
                             required=True)
    service_tag = fields.Char(max_length=30,
                              string="Etiqueta de Serviço (Dell)")
    buy_date = fields.Date(string="Data de Compra")
    guarantee_control = fields.Selection([
        ('yes', 'Sim'),
        ('no', 'Não'), ],
        string="Controla Garantia?",
        required=True)
    gurantee_period = fields.Char(max_length=30, string="Prazo de Garantia")
    processor = fields.Char(max_length=30, string="Processador",
                            required=True)
    memory = fields.Char(max_length=30, string="Memória", required=True)
    hd = fields.Char(max_length=30, string="HD", required=True)
    motherboard_manufacturer = fields.Char(
        max_length=30, string="Fabricante e Modelo da Placa Mãe")
    equipment_name = fields.Char(max_length=30,
                                 string="Nome do Equipamento na Rede",
                                 required=True)
    web_type = fields.Selection([
        ('1', 'Grupo de Trabalho'),
        ('2', 'Domínio'), ],
        string="Tipo de Rede",
        required=True)
    web_name = fields.Char(max_length=30, string="Nome da Rede", required=True)
    user_local_login = fields.Char(
        max_length=30,
        string="Login usuário administrador local",
        required=True)
    user_local_password = fields.Char(
        max_length=30,
        string="Senha usuário administrador local",
        required=True)
    ip_type = fields.Selection([
        ('1', 'Fornecido po DHCP'),
        ('2', 'IP Fixo na Placa'), ],
        string="Tipo de endereço de IP",
        required=True)
    mac_address = fields.Char(max_length=30,
                              string="Endereço Físico (Mac Adress)",
                              required=True)
    ip_address = fields.Char(max_length=30, string="Endereço IP (rede local)",
                             required=True)
    sub_web_mask = fields.Char(max_length=30, string="Mascará sub-rede",
                               required=True)
    gateway = fields.Char(max_length=30, string="Gateway", required=True)
    dns1 = fields.Char(max_length=30, string="DNS1", required=True)
    dns2 = fields.Char(max_length=30, string="DNS2", required=True)
    remote_access_door = fields.Char(
        max_length=30, string="Número de Porta de Acesso Remoto")
    server_print = fields.Selection([
        ('1', 'SIM'),
        ('2', 'NÃO'), ],
        string="Servidor de Impressão",
        required=True)
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
        string="Usa E-mail?",
        required=True)
    email_use_type = fields.Selection([
        ('1', 'Webmail'),
        ('2', 'Outlook'),
        ('3', 'Outros'), ],
        string="Forma de Uso de E-mail",
        required=True)
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
    op_system = fields.Char(max_length=30, string="Sistema Operacional",
                            required=True)
    op_system_version = fields.Char(max_length=30,
                                    string="Versão do Sistema Operacional",
                                    required=True)
    antivirus = fields.Char(max_length=30, string="Antivírus", required=True)
    antivirus_version = fields.Char(max_length=30,
                                    string="Versão do Antivírus",
                                    required=True)
    tag_server = fields.Integer(string="Etiqueta", required=True)
    remote_acces_path_ts = fields.Char(max_length=30,
                                       string="Rota de Acesso Remoto via TS")
    ts_remote_access_door = fields.Integer(string="Porta de Acesso Remoto TS")
    service_tag_server = fields.Char(max_length=30,
                                     string="Etiqueta de Serviço (Dell)",
                                     required=True)
    server_function = fields.Char(max_length=50, string="Função do Servidor",
                                  required=True)
    admin_user_login = fields.Char(max_length=30,
                                   string="Login do Usuário Administrador",
                                   required=True)
    admin_user_password = fields.Char(max_length=30,
                                      string="Login do Usuário Administrador",
                                      required=True)
    other_info_and_obs = fields.Text(string="Outras Informações e Observações")
    tag_mobile = fields.Integer(string="Etiqueta", required=True)
    mobile_equipment_type = fields.Char(max_length=30,
                                        string="Tipo de Equipamento",
                                        required=True)
    tag_accessories = fields.Integer(string="Etiqueta", required=True)
    accessories_equipment_type = fields.Char(max_length=30,
                                             string="Tipo de Equipamento",
                                             required=True)
    tag_net_equipment = fields.Integer(string="Etiqueta", required=True)
    net_equipment_type = fields.Char(max_length=30,
                                     string="Tipo de Equipamento",
                                     required=True)
    tag_tel_equipment = fields.Integer(string="Etiqueta", required=True)
    tel_equipment_type = fields.Char(max_length=30,
                                     string="Tipo de Equipamento",
                                     required=True)
    tag_cftv_equipment = fields.Integer(string="Etiqueta", required=True)
    cftv_equipment_type = fields.Char(max_length=30,
                                      string="Tipo de Equipamento",
                                      required=True)
    tag_others = fields.Integer(string="Etiqueta", required=True)
    other_equipment_type = fields.Char(max_length=30,
                                       string="Tipo de Equipamento",
                                       required=True)
