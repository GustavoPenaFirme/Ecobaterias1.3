from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Arrecadacao, PontoColeta

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/painel")
@login_required
def painel():
    arrecadacoes = (
        Arrecadacao.query.filter_by(user_id=current_user.id)
        .order_by(Arrecadacao.data.desc())
        .limit(20)
        .all()
    )
    total = (
        db.session.query(db.func.coalesce(db.func.sum(Arrecadacao.peso_kg), 0.0))
        .filter_by(user_id=current_user.id)
        .scalar()
    )
    qtd = Arrecadacao.query.filter_by(user_id=current_user.id).count()
    pontos = PontoColeta.query.order_by(PontoColeta.nome).all()
    return render_template(
        "painel.html",
        arrecadacoes=arrecadacoes,
        total_kg=round(float(total or 0), 2),
        qtd=qtd,
        pontos=pontos,
    )


@bp.route("/arrecadacao", methods=["POST"])
@login_required
def nova_arrecadacao():
    tipo = (request.form.get("tipo_material") or "").strip()
    peso = request.form.get("peso_kg")
    regiao = (request.form.get("regiao") or "").strip()
    obs = (request.form.get("obs") or "").strip()
    ponto_id = request.form.get("ponto_id") or None

    try:
        peso_f = float(str(peso).replace(",", "."))
    except (TypeError, ValueError):
        flash("Informe um peso vÃ¡lido.", "warning")
        return redirect(url_for("main.painel"))

    if not tipo or peso_f <= 0:
        flash("Preencha tipo de material e peso corretamente.", "warning")
        return redirect(url_for("main.painel"))

    ar = Arrecadacao(
        user_id=current_user.id,
        tipo_material=tipo,
        peso_kg=peso_f,
        regiao=regiao or None,
        obs=obs or None,
        ponto_id=int(ponto_id) if ponto_id else None,
    )
    db.session.add(ar)
    db.session.commit()
    flash("ArrecadaÃ§Ã£o registrada com sucesso!", "success")
    return redirect(url_for("main.painel"))


@bp.route("/mapa")
@login_required
def mapa():
    pontos = PontoColeta.query.order_by(PontoColeta.nome).all()
    return render_template("mapa.html", pontos=pontos)

