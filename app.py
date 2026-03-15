import os
from flask import Flask, jsonify
from models import db
from routes import bp


def create_app(config=None):
    app = Flask(__name__)

    # Configuração do banco de dados
    db_path = os.path.join(os.path.dirname(__file__), "instance", "empreendimentos.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config.setdefault("SQLALCHEMY_DATABASE_URI", f"sqlite:///{db_path}")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    if config:
        app.config.update(config)

    db.init_app(app)

    app.register_blueprint(bp)

    # Rota raiz com informações da API
    @app.route("/")
    def index():
        return jsonify(
            {
                "api": "Empreendimentos SC",
                "versao": "1.0.0",
                "descricao": "API REST para gerenciamento de empreendimentos em Santa Catarina",
                "endpoints": {
                    "listar": "GET  /api/empreendimentos",
                    "obter": "GET  /api/empreendimentos/<id>",
                    "criar": "POST /api/empreendimentos",
                    "atualizar": "PUT  /api/empreendimentos/<id>",
                    "remover": "DELETE /api/empreendimentos/<id>",
                    "segmentos": "GET  /api/empreendimentos/meta/segmentos",
                    "status": "GET  /api/empreendimentos/meta/status",
                },
            }
        )

    # Tratamento de erros globais
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": str(e)}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"erro": "Método HTTP não permitido."}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"erro": "Erro interno no servidor."}), 500

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
