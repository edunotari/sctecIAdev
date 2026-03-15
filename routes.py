from flask import Blueprint, jsonify, request
from models import db, Empreendimento, SEGMENTOS_VALIDOS, STATUS_VALIDOS
from datetime import datetime

bp = Blueprint("empreendimentos", __name__, url_prefix="/api/empreendimentos")


def _erro(mensagem, codigo=400):
    return jsonify({"erro": mensagem}), codigo


def _validar_campos(dados, parcial=False):
    """Valida os campos obrigatórios e retorna mensagem de erro ou None."""
    campos_obrigatorios = ["nome", "empreendedor", "municipio", "segmento", "contato"]

    if not parcial:
        faltando = [c for c in campos_obrigatorios if not dados.get(c, "").strip()]
        if faltando:
            return f"Campos obrigatórios ausentes ou vazios: {', '.join(faltando)}"

    if "segmento" in dados and dados["segmento"] not in SEGMENTOS_VALIDOS:
        return (
            f"Segmento inválido. Opções: {', '.join(sorted(SEGMENTOS_VALIDOS))}"
        )

    if "status" in dados and dados["status"] not in STATUS_VALIDOS:
        return "Status inválido. Use 'ativo' ou 'inativo'."

    if "data_fundacao" in dados and dados["data_fundacao"]:
        try:
            datetime.strptime(dados["data_fundacao"], "%Y-%m-%d")
        except ValueError:
            return "data_fundacao inválida. Use o formato YYYY-MM-DD."

    return None


# ---------------------------------------------------------------------------
# GET /api/empreendimentos
# Suporta filtros via query string: status, segmento, municipio, q (busca livre)
# ---------------------------------------------------------------------------
@bp.route("", methods=["GET"])
def listar():
    query = Empreendimento.query

    status = request.args.get("status")
    if status:
        if status not in STATUS_VALIDOS:
            return _erro(f"Filtro 'status' inválido. Use: {', '.join(STATUS_VALIDOS)}")
        query = query.filter_by(status=status)

    segmento = request.args.get("segmento")
    if segmento:
        if segmento not in SEGMENTOS_VALIDOS:
            return _erro(
                f"Filtro 'segmento' inválido. Opções: {', '.join(sorted(SEGMENTOS_VALIDOS))}"
            )
        query = query.filter_by(segmento=segmento)

    municipio = request.args.get("municipio")
    if municipio:
        query = query.filter(
            Empreendimento.municipio.ilike(f"%{municipio}%")
        )

    q = request.args.get("q")
    if q:
        termo = f"%{q}%"
        query = query.filter(
            db.or_(
                Empreendimento.nome.ilike(termo),
                Empreendimento.empreendedor.ilike(termo),
                Empreendimento.municipio.ilike(termo),
            )
        )

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    paginado = query.order_by(Empreendimento.nome).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "total": paginado.total,
            "pagina": paginado.page,
            "por_pagina": paginado.per_page,
            "paginas": paginado.pages,
            "dados": [e.to_dict() for e in paginado.items],
        }
    )


# ---------------------------------------------------------------------------
# GET /api/empreendimentos/<id>
# ---------------------------------------------------------------------------
@bp.route("/<int:id>", methods=["GET"])
def obter(id):
    emp = db.get_or_404(Empreendimento, id, description="Empreendimento não encontrado.")
    return jsonify(emp.to_dict())


# ---------------------------------------------------------------------------
# POST /api/empreendimentos
# ---------------------------------------------------------------------------
@bp.route("", methods=["POST"])
def criar():
    dados = request.get_json(silent=True)
    if not dados:
        return _erro("Corpo da requisição deve ser JSON.")

    erro = _validar_campos(dados, parcial=False)
    if erro:
        return _erro(erro)

    emp = Empreendimento(
        nome=dados["nome"].strip(),
        empreendedor=dados["empreendedor"].strip(),
        municipio=dados["municipio"].strip(),
        segmento=dados["segmento"],
        contato=dados["contato"].strip(),
        status=dados.get("status", "ativo"),
        descricao=dados.get("descricao", "").strip() or None,
        data_fundacao=dados.get("data_fundacao") or None,
    )
    db.session.add(emp)
    db.session.commit()
    return jsonify(emp.to_dict()), 201


# ---------------------------------------------------------------------------
# PUT /api/empreendimentos/<id>
# ---------------------------------------------------------------------------
@bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    emp = db.get_or_404(Empreendimento, id, description="Empreendimento não encontrado.")

    dados = request.get_json(silent=True)
    if not dados:
        return _erro("Corpo da requisição deve ser JSON.")

    erro = _validar_campos(dados, parcial=True)
    if erro:
        return _erro(erro)

    campos_texto = ["nome", "empreendedor", "municipio", "contato"]
    for campo in campos_texto:
        if campo in dados:
            setattr(emp, campo, dados[campo].strip())

    for campo in ["segmento", "status"]:
        if campo in dados:
            setattr(emp, campo, dados[campo])

    if "descricao" in dados:
        emp.descricao = dados["descricao"].strip() or None

    if "data_fundacao" in dados:
        emp.data_fundacao = dados["data_fundacao"] or None

    emp.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(emp.to_dict())


# ---------------------------------------------------------------------------
# DELETE /api/empreendimentos/<id>
# ---------------------------------------------------------------------------
@bp.route("/<int:id>", methods=["DELETE"])
def remover(id):
    emp = db.get_or_404(Empreendimento, id, description="Empreendimento não encontrado.")
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"mensagem": f"Empreendimento '{emp.nome}' removido com sucesso."})


# ---------------------------------------------------------------------------
# GET /api/empreendimentos/segmentos  — valores aceitos para segmento
# GET /api/empreendimentos/status     — valores aceitos para status
# ---------------------------------------------------------------------------
@bp.route("/meta/segmentos", methods=["GET"])
def segmentos():
    return jsonify({"segmentos": sorted(SEGMENTOS_VALIDOS)})


@bp.route("/meta/status", methods=["GET"])
def status_list():
    return jsonify({"status": sorted(STATUS_VALIDOS)})
