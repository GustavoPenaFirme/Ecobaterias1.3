from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    perfil = db.Column(db.String(20), default="usuario")  # usuario | admin
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    arrecadacoes = db.relationship("Arrecadacao", backref="usuario", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.perfil == "admin"


class PontoColeta(db.Model):
    __tablename__ = "pontos_coleta"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    cidade = db.Column(db.String(100), default="Brasília")
    uf = db.Column(db.String(2), default="DF")
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default="Aberto")  # Aberto | Fechado
    responsavel_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    arrecadacoes = db.relationship("Arrecadacao", backref="ponto", lazy=True)
    solicitacoes = db.relationship("SolicitacaoRetirada", backref="ponto", lazy=True)


class Arrecadacao(db.Model):
    __tablename__ = "arrecadacoes"

    id = db.Column(db.Integer, primary_key=True)
    ponto_id = db.Column(db.Integer, db.ForeignKey("pontos_coleta.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tipo_material = db.Column(db.String(120), nullable=False)
    peso_kg = db.Column(db.Float, nullable=False)
    regiao = db.Column(db.String(200), nullable=True)
    obs = db.Column(db.Text, nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)


class SolicitacaoRetirada(db.Model):
    __tablename__ = "solicitacoes_retirada"

    id = db.Column(db.Integer, primary_key=True)
    ponto_id = db.Column(db.Integer, db.ForeignKey("pontos_coleta.id"), nullable=False)
    volume_kg = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default="Pendente")  # Pendente | Agendada | Concluida
    data_solicitacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_retirada = db.Column(db.DateTime, nullable=True)
