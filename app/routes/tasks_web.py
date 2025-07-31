"""from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
    flash,
    redirect,
    url_for
)
from flask_login import login_required, current_user
from app.services.task_service import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    toggle_task_completion
)

tasks = Blueprint("tasks", __name__)

@tasks.route("/")
@tasks.route("/index")
@login_required
def index():

    try:
        user_tasks = get_all_tasks(current_user.id)
        return render_template("tasks/index.html", tasks=user_tasks)
    except Exception as e:
        flash(f"Error al cargar las tareas: {str(e)}", "error")
        return render_template("tasks/index.html", tasks=[])

@tasks.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        priority_id = request.form.get("priority_id")
        category_id = request.form.get("category_id")
        
        try:
            new_task = create_task(
                title=title,
                description=description,
                due_date=due_date,
                priority_id=priority_id,
                category_id=category_id,
                user_id=current_user.id
            )
            flash("Tarea creada exitosamente", "success")
            return redirect(url_for("tasks.index"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("tasks.create"))
    
    return render_template("tasks/create.html")

@tasks.route("/<int:task_id>")
@login_required
def view(task_id):

    try:
        task = get_task_by_id(task_id, current_user.id)
        return render_template("tasks/view.html", task=task)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("tasks.index"))

@tasks.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit(task_id):
    try:
        task = get_task_by_id(task_id, current_user.id)
        
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            due_date = request.form.get("due_date")
            priority_id = request.form.get("priority_id")
            category_id = request.form.get("category_id")
            
            updated_task = update_task(
                task_id=task_id,
                title=title,
                description=description,
                due_date=due_date,
                priority_id=priority_id,
                category_id=category_id,
                user_id=current_user.id
            )
            flash("Tarea actualizada exitosamente", "success")
            return redirect(url_for("tasks.view", task_id=task_id))
        
        return render_template("tasks/edit.html", task=task)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("tasks.index"))

@tasks.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete(task_id):
    try:
        delete_task(task_id, current_user.id)
        flash("Tarea eliminada exitosamente", "success")
    except ValueError as e:
        flash(str(e), "error")
    
    return redirect(url_for("tasks.index"))

@tasks.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle(task_id):
    try:
        task = toggle_task_completion(task_id, current_user.id)
        estado = "completada" if task.is_completed else "pendiente"
        flash(f"Tarea marcada como {estado}", "success")
    except ValueError as e:
        flash(str(e), "error")
    
    return redirect(url_for("tasks.index")) """