from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

SEGMENTOS_VALIDOS = {"Tecnologia", "Comércio", "Indústria", "Serviços", "Agronegócio"}
STATUS_VALIDOS = {"ativo", "inativo"}

# Todos os campos de texto opcionais (usados pelo routes para SET genérico)
CAMPOS_OPCIONAIS = [
    # básicos opcionais
    "descricao",
    # identificação e localização
    "razao_social", "nome_fantasia", "cnpj", "data_abertura",
    "inscricao_estadual", "inscricao_municipal",
    "endereco", "link_maps", "tipo_unidade",
    "email_nfe", "telefone", "responsavel_cadastro",
    # fiscal / financeiro / societário
    "regime_tributario", "cnae", "dados_bancarios",
    "faturamento_medio", "prazo_pagamento",
    "qsa", "capital_social", "verificacao_pep", "certidoes_negativas",
    # setor: Tecnologia
    "tec_seguranca_lgpd", "tec_stack",
    # setor: Comércio
    "com_subst_tributaria", "com_logistica",
    # setor: Indústria
    "ind_licencas", "ind_capacidade",
    # setor: Serviços
    "serv_conselhos", "serv_portfolio",
    # setor: Agronegócio
    "agro_car", "agro_armazenagem",
    # documentação
    "checklist_docs",
]


class Empreendimento(db.Model):
    __tablename__ = "empreendimentos"

    # ── Campos obrigatórios ────────────────────────────────────────
    id           = db.Column(db.Integer, primary_key=True)
    nome         = db.Column(db.String(200), nullable=False)
    empreendedor = db.Column(db.String(200), nullable=False)
    municipio    = db.Column(db.String(100), nullable=False)
    segmento     = db.Column(db.String(50),  nullable=False)
    contato      = db.Column(db.String(200), nullable=False)
    status       = db.Column(db.String(10),  nullable=False, default="ativo")

    # ── Identificação e Localização ────────────────────────────────
    razao_social         = db.Column(db.String(200), nullable=True)
    nome_fantasia        = db.Column(db.String(200), nullable=True)
    cnpj                 = db.Column(db.String(20),  nullable=True)
    data_abertura        = db.Column(db.String(10),  nullable=True)
    inscricao_estadual   = db.Column(db.String(50),  nullable=True)
    inscricao_municipal  = db.Column(db.String(50),  nullable=True)
    endereco             = db.Column(db.String(500), nullable=True)
    link_maps            = db.Column(db.String(500), nullable=True)
    tipo_unidade         = db.Column(db.String(20),  nullable=True)   # Matriz / Filial
    email_nfe            = db.Column(db.String(200), nullable=True)
    telefone             = db.Column(db.String(50),  nullable=True)
    responsavel_cadastro = db.Column(db.String(200), nullable=True)

    # ── Dados Fiscais, Financeiros e Societários ───────────────────
    regime_tributario  = db.Column(db.String(50),  nullable=True)
    cnae               = db.Column(db.String(30),  nullable=True)
    dados_bancarios    = db.Column(db.Text,        nullable=True)
    faturamento_medio  = db.Column(db.String(100), nullable=True)
    prazo_pagamento    = db.Column(db.String(100), nullable=True)
    qsa                = db.Column(db.Text,        nullable=True)
    capital_social     = db.Column(db.String(100), nullable=True)
    verificacao_pep    = db.Column(db.String(10),  nullable=True)   # Sim / Não
    certidoes_negativas= db.Column(db.Text,        nullable=True)

    # ── Campos Específicos — Tecnologia ───────────────────────────
    tec_seguranca_lgpd = db.Column(db.Text, nullable=True)
    tec_stack          = db.Column(db.Text, nullable=True)

    # ── Campos Específicos — Comércio ─────────────────────────────
    com_subst_tributaria = db.Column(db.Text, nullable=True)
    com_logistica        = db.Column(db.Text, nullable=True)

    # ── Campos Específicos — Indústria ────────────────────────────
    ind_licencas   = db.Column(db.Text, nullable=True)
    ind_capacidade = db.Column(db.Text, nullable=True)

    # ── Campos Específicos — Serviços ─────────────────────────────
    serv_conselhos = db.Column(db.Text, nullable=True)
    serv_portfolio = db.Column(db.Text, nullable=True)

    # ── Campos Específicos — Agronegócio ──────────────────────────
    agro_car        = db.Column(db.String(100), nullable=True)
    agro_armazenagem= db.Column(db.Text,        nullable=True)

    # ── Documentação ──────────────────────────────────────────────
    descricao     = db.Column(db.Text, nullable=True)
    checklist_docs= db.Column(db.Text, nullable=True)

    # ── Datas legadas ─────────────────────────────────────────────
    data_fundacao = db.Column(db.String(10),  nullable=True)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime,    default=datetime.utcnow,
                              onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":           self.id,
            "nome":         self.nome,
            "empreendedor": self.empreendedor,
            "municipio":    self.municipio,
            "segmento":     self.segmento,
            "contato":      self.contato,
            "status":       self.status,
            # identificação/localização
            "razao_social":         self.razao_social,
            "nome_fantasia":        self.nome_fantasia,
            "cnpj":                 self.cnpj,
            "data_abertura":        self.data_abertura,
            "inscricao_estadual":   self.inscricao_estadual,
            "inscricao_municipal":  self.inscricao_municipal,
            "endereco":             self.endereco,
            "link_maps":            self.link_maps,
            "tipo_unidade":         self.tipo_unidade,
            "email_nfe":            self.email_nfe,
            "telefone":             self.telefone,
            "responsavel_cadastro": self.responsavel_cadastro,
            # fiscal
            "regime_tributario":   self.regime_tributario,
            "cnae":                self.cnae,
            "dados_bancarios":     self.dados_bancarios,
            "faturamento_medio":   self.faturamento_medio,
            "prazo_pagamento":     self.prazo_pagamento,
            "qsa":                 self.qsa,
            "capital_social":      self.capital_social,
            "verificacao_pep":     self.verificacao_pep,
            "certidoes_negativas": self.certidoes_negativas,
            # setor
            "tec_seguranca_lgpd":  self.tec_seguranca_lgpd,
            "tec_stack":           self.tec_stack,
            "com_subst_tributaria":self.com_subst_tributaria,
            "com_logistica":       self.com_logistica,
            "ind_licencas":        self.ind_licencas,
            "ind_capacidade":      self.ind_capacidade,
            "serv_conselhos":      self.serv_conselhos,
            "serv_portfolio":      self.serv_portfolio,
            "agro_car":            self.agro_car,
            "agro_armazenagem":    self.agro_armazenagem,
            # extras
            "descricao":      self.descricao,
            "checklist_docs": self.checklist_docs,
            "data_fundacao":  self.data_fundacao,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
