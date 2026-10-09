from flask import Blueprint, flash, redirect, render_template, request, session, url_for

import database
from seguranca import exigir_login


leituras_bp = Blueprint("leituras", __name__)


@leituras_bp.route("/leituras")
def index():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    usuario_id = session.get("usuario_id")
    leituras = database.listar_leituras(usuario_id)
    return render_template("leituras.html", leituras=leituras)


@leituras_bp.route("/leituras/nova", methods=["GET", "POST"])
def nova_leitura():
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        paginas = int(request.form["paginas"])
        database.criar_leitura(titulo, autor, paginas, session["usuario_id"])
        flash("Leitura cadastrada.")
        return redirect(url_for("leituras.index"))

    return render_template("nova_leitura.html")


def buscar_leitura_do_usuario(leitura_id):
    usuario_id = session.get("usuario_id")
    leitura = database.buscar_leitura(leitura_id, usuario_id)
    if leitura is not None:
        return leitura

    leitura_existente = database.buscar_leitura(leitura_id)
    if leitura_existente is None:
        return None

    flash("você não pode acessar uma leitura que não é sua")
    return "proibido"


@leituras_bp.route("/leituras/<int:leitura_id>/editar", methods=["GET", "POST"])
def editar_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    leitura = buscar_leitura_do_usuario(leitura_id)
    if leitura is None:
        return "leitura não encontrada", 404
    if leitura == "proibido":
        return redirect(url_for("leituras.index"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        paginas = int(request.form["paginas"])
        database.atualizar_leitura(leitura_id, session["usuario_id"], titulo, autor, paginas)
        flash("Leitura atualizada.")
        return redirect(url_for("leituras.index"))

    return render_template("editar_leitura.html", leitura=leitura)


@leituras_bp.post("/leituras/<int:leitura_id>/concluir")
def concluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    leitura = buscar_leitura_do_usuario(leitura_id)
    if leitura is None:
        return "leitura não encontrada", 404
    if leitura == "proibido":
        return redirect(url_for("leituras.index"))

    database.alternar_concluida(leitura_id, session["usuario_id"])
    flash("Status da leitura atualizado.")
    return redirect(url_for("leituras.index"))


@leituras_bp.post("/leituras/<int:leitura_id>/excluir")
def excluir_leitura(leitura_id):
    bloqueio = exigir_login()
    if bloqueio:
        return bloqueio

    leitura = buscar_leitura_do_usuario(leitura_id)
    if leitura is None:
        return "leitura não encontrada", 404
    if leitura == "proibido":
        return redirect(url_for("leituras.index"))

    database.excluir_leitura(leitura_id, session["usuario_id"])
    flash("Leitura excluída.")
    return redirect(url_for("leituras.index"))
