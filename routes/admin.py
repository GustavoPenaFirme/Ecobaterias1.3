from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, User, PontoColeta, Arrecadacao, SolicitacaoRetirada

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)

    return decorated


@bp.route("/")
@login_required
@admin_required
def dashboard():
    pontos_ativos = PontoColeta.query.filter_by(status="Aberto").count()
    total_arrec = Arrecadacao.query.count()
    volume = db.session.query(db.func.coalesce(db.func.sum(Arrecadacao.peso_kg), 0.0)).scalar()
    pendentes = SolicitacaoRetirada.query.filter_by(status="Pendente").count()
    solicitacoes = (
        SolicitacaoRetirada.query.order_by(SolicitacaoRetirada.data_solicitacao.desc())
        .limit(15)
        .all()
    )
    return render_template(
        "admin.html",
        pontos_ativos=pontos_ativos,
        total_arrec=total_arrec,
        volume=round(float(volume or 0), 2),
        pendentes=pendentes,
        solicitacoes=solicitacoes,
    )


@bp.route("/solicitacao/<int:sid>/aprovar", methods=["POST"])
@login_required
@admin_required
def aprovar(sid):
    s = db.session.get(SolicitacaoRetirada, sid)
    if not s:
        flash("SolicitaÃ§Ã£o nÃ£o encontrada.", "warning")
        return redirect(url_for("admin.dashboard"))
    s.status = "Agendada"
    db.session.commit()
    flash(f"SolicitaÃ§Ã£o #{sid} aprovada/agendada.", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/ponto", methods=["POST"])
@login_required
@admin_required
def novo_ponto():
    nome = (request.form.get("nome") or "").strip()
    endereco = (request.form.get("endereco") or "").strip()
    cidade = (request.form.get("cidade") or "BrasÃ­lia").strip()
    if not nome or not endereco:
        flash("Nome e endereÃ§o sÃ£o obrigatÃ³rios.", "warning")
        return redirect(url_for("admin.dashboard"))
    p = PontoColeta(nome=nome, endereco=endereco, cidade=cidade, status="Aberto")
    db.session.add(p)
    db.session.commit()
    flash("Ponto de coleta cadastrado.", "success")
    return redirect(url_for("admin.dashboard"))

