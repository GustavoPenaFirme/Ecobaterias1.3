from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from routes.auth import bp as auth_bp
    from routes.main import bp as main_bp
    from routes.admin import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    return app


def _seed_if_empty():
    """Cria admin padrão e pontos de exemplo se o banco estiver vazio."""
    if User.query.first():
        return

    admin = User(email="admin@ecobateria.app", nome="Administrador", perfil="admin")
    admin.set_password("admin123")
    db.session.add(admin)

    demo = User(email="pena.gustavo@gmail.com", nome="Gustavo Pena", perfil="usuario")
    demo.set_password("senha123")
    db.session.add(demo)

    from models import PontoColeta

    pontos = [
        PontoColeta(
            nome="Ponto Asa Norte – Coleta DF",
            endereco="SQN 108, Asa Norte",
            cidade="Brasília",
            uf="DF",
            lat=-15.7600,
            lng=-47.8800,
            status="Aberto",
        ),
        PontoColeta(
            nome="Ecoponto Asa Sul",
            endereco="CLS 402, Asa Sul",
            cidade="Brasília",
            uf="DF",
            lat=-15.8200,
            lng=-47.9100,
            status="Aberto",
        ),
        PontoColeta(
            nome="Cooperativa Taguatinga",
            endereco="QNA 15, Taguatinga Norte",
            cidade="Brasília",
            uf="DF",
            lat=-15.8300,
            lng=-48.0500,
            status="Aberto",
        ),
        PontoColeta(
            nome="Loja Parceira Sudoeste",
            endereco="CLSW 103, Sudoeste",
            cidade="Brasília",
            uf="DF",
            lat=-15.7950,
            lng=-47.9250,
            status="Fechado",
        ),
    ]
    for p in pontos:
        db.session.add(p)

    db.session.commit()


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, host="0.0.0.0", port=5000)
