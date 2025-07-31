from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.services.task_service import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion,
)

task_views = Blueprint("task_views", __name__, url_prefix="/tasks")

@task_views.route("/")
def index():
    return render_template("tasks/index.html")


@task_views.route("/", methods=["GET"])
@login_required
def list_tasks():
    result = get_all_tasks(user_id=current_user.id)
    tasks = result.get("data", []) if result.get("success") else []
    return render_template("tasks/list.html", tasks=tasks)


@task_views.route("/<int:task_id>", methods=["GET"])
@login_required
def task_detail(task_id):
    result = get_task_by_id(task_id, user_id=current_user.id)
    task = result.get("data") if result.get("success") else None
    if not task:
        flash("Tarea no encontrada", "warning")
        return redirect(url_for("task_views.list_tasks"))
    return render_template("tasks/detail.html", task=task)


@task_views.route("/nuevo", methods=["GET", "POST"])
@login_required
def create_task_view():
    if request.method == "POST":
        data = request.form
        result = create_task(
            title=data.get("title"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            priority_id=data.get("priority_id"),
            category_id=data.get("category_id"),
            user_id=current_user.id
        )
        if result.get("success"):
            flash("Tarea creada exitosamente", "success")
            return redirect(url_for("task_views.list_tasks"))
        else:
            flash(result.get("message", "Error al crear la tarea"), "danger")
    
    return render_template("tasks/create.html")


@task_views.route("/<int:task_id>/editar", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    result = get_task_by_id(task_id, user_id=current_user.id)
    task = result.get("data") if result.get("success") else None
    if not task:
        flash("Tarea no encontrada", "warning")
        return redirect(url_for("task_views.list_tasks"))

    if request.method == "POST":
        data = request.form
        update_result = update_task(
            task_id=task_id,
            title=data.get("title"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            priority_id=data.get("priority_id"),
            category_id=data.get("category_id"),
            user_id=current_user.id
        )
        if update_result.get("success"):
            flash("Tarea actualizada", "success")
            return redirect(url_for("task_views.list_tasks"))
        else:
            flash(update_result.get("message", "Error al actualizar"), "danger")
    
    return render_template("tasks/edit.html", task=task)


@task_views.route("/<int:task_id>/eliminar", methods=["POST"])
@login_required
def delete_task_view(task_id):
    result = delete_task(task_id=task_id, user_id=current_user.id)
    flash(result.get("message", "Tarea eliminada"), "success" if result.get("success") else "danger")
    return redirect(url_for("task_views.list_tasks"))


@task_views.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_status(task_id):
    result = toggle_task_completion(task_id=task_id, user_id=current_user.id)
    flash("Estado cambiado", "success" if result.get("success") else "danger")
    return redirect(url_for("task_views.list_tasks"))
