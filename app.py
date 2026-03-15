import os
from flask import Flask, jsonify, render_template
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

    # Dashboard (interface gráfica)
    @app.route("/")
    def index():
        return render_template("index.html")

    # Informações da API em JSON
    @app.route("/api")
    def api_info():
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
        _migrar_colunas(app)

    return app


def _migrar_colunas(app):
    """Adiciona colunas novas em bancos SQLite já existentes sem perder dados."""
    from sqlalchemy import inspect, text

    novas = {
        "razao_social": "VARCHAR(200)", "nome_fantasia": "VARCHAR(200)",
        "cnpj": "VARCHAR(20)", "data_abertura": "VARCHAR(10)",
        "inscricao_estadual": "VARCHAR(50)", "inscricao_municipal": "VARCHAR(50)",
        "endereco": "VARCHAR(500)", "link_maps": "VARCHAR(500)",
        "tipo_unidade": "VARCHAR(20)", "email_nfe": "VARCHAR(200)",
        "telefone": "VARCHAR(50)", "responsavel_cadastro": "VARCHAR(200)",
        "regime_tributario": "VARCHAR(50)", "cnae": "VARCHAR(30)",
        "dados_bancarios": "TEXT", "faturamento_medio": "VARCHAR(100)",
        "prazo_pagamento": "VARCHAR(100)", "qsa": "TEXT",
        "capital_social": "VARCHAR(100)", "verificacao_pep": "VARCHAR(10)",
        "certidoes_negativas": "TEXT",
        "tec_seguranca_lgpd": "TEXT", "tec_stack": "TEXT",
        "com_subst_tributaria": "TEXT", "com_logistica": "TEXT",
        "ind_licencas": "TEXT", "ind_capacidade": "TEXT",
        "serv_conselhos": "TEXT", "serv_portfolio": "TEXT",
        "agro_car": "VARCHAR(100)", "agro_armazenagem": "TEXT",
        "checklist_docs": "TEXT",
    }
    engine = db.engine
    existentes = {c["name"] for c in inspect(engine).get_columns("empreendimentos")}
    with engine.connect() as conn:
        for col, tipo in novas.items():
            if col not in existentes:
                conn.execute(text(f"ALTER TABLE empreendimentos ADD COLUMN {col} {tipo}"))
        conn.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
