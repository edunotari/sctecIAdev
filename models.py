from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

SEGMENTOS_VALIDOS = {"Tecnologia", "Comércio", "Indústria", "Serviços", "Agronegócio"}
STATUS_VALIDOS = {"ativo", "inativo"}


class Empreendimento(db.Model):
    __tablename__ = "empreendimentos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    empreendedor = db.Column(db.String(200), nullable=False)
    municipio = db.Column(db.String(100), nullable=False)
    segmento = db.Column(db.String(50), nullable=False)
    contato = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="ativo")
    descricao = db.Column(db.Text, nullable=True)
    data_fundacao = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "empreendedor": self.empreendedor,
            "municipio": self.municipio,
            "segmento": self.segmento,
            "contato": self.contato,
            "status": self.status,
            "descricao": self.descricao,
            "data_fundacao": self.data_fundacao,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
