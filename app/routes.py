from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Appointment
from datetime import datetime

main = Blueprint("main", __name__)


# HOME
@main.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        name = request.form["name"]
        service = request.form["service"]

        date_str = request.form["date"]
        time_str = request.form["time"]

        data_formatada = datetime.strptime(date_str, "%Y-%m-%d").date()
        hora_formatada = datetime.strptime(time_str, "%H:%M").time()

        # Verifica conflito
        existe = Appointment.query.filter_by(
            date=data_formatada,
            time=hora_formatada
        ).first()

        if existe:
            flash("Esse horário já está ocupado!", "error")
            return redirect(url_for("main.home"))

        novo = Appointment(
            name=name,
            service=service,
            date=data_formatada,
            time=hora_formatada
        )

        db.session.add(novo)
        db.session.commit()

        flash("Agendamento criado!", "success")
        return redirect(url_for("main.home"))

    appointments = Appointment.query.order_by(
        Appointment.date,
        Appointment.time
    ).all()

    return render_template("index.html", appointments=appointments)


# EDITAR
@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    agendamento = Appointment.query.get_or_404(id)

    if request.method == "POST":

        agendamento.name = request.form["name"]
        agendamento.service = request.form["service"]

        date_str = request.form["date"]
        time_str = request.form["time"]

        agendamento.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        agendamento.time = datetime.strptime(time_str, "%H:%M").time()

        db.session.commit()

        flash("Agendamento atualizado!", "success")
        return redirect(url_for("main.home"))

    return render_template("edit.html", a=agendamento)

@main.route("/delete/<int:id>")
def delete(id):
    
    agendamento = Appointment.query.get_or_404(id)

    db.session.delete(agendamento)
    db.session.commit()

    flash("Agendamento  removido!","success")
    return redirect(url_for("main.home"))