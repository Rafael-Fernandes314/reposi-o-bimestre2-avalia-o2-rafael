from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        if email and database.buscar_usuario_por_email(email):
            flash("email já é usado")
            return redirect(url_for("auth.registro"))
        senha_hash = generate_password_hash(senha)
        database.criar_usuario(nome, email, senha_hash)
        return redirect(url_for("auth.login"))
    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        usuario = database.buscar_usuario_por_email(email)
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            return redirect(url_for("leituras.index"))
        flash("email ou senha errados")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("usuario_id", None)
    session.pop("usuario_nome", None)
    return redirect(url_for("auth.login"))
