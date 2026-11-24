from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.painel"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            flash("Login realizado com sucesso.", "success")
            if user.is_admin():
                return redirect(next_page or url_for("admin.dashboard"))
            return redirect(next_page or url_for("main.painel"))
        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html")


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for("main.painel"))

    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        if not nome or not email or not password:
            flash("Preencha todos os campos.", "warning")
            return render_template("cadastro.html")
        if User.query.filter_by(email=email).first():
            flash("Este e-mail já está cadastrado.", "warning")
            return render_template("cadastro.html")
        user = User(nome=nome, email=email, perfil="usuario")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Cadastro realizado. Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("cadastro.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("main.index"))

