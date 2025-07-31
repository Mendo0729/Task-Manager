import logging
from unittest import result

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from flask_login import current_user, login_required

from app.services.task_service import (
    create_task,
    delete_task,
    get_all_tasks,
    get_completed_tasks,
    get_pending_tasks,
    get_task_by_id,
    get_tasks_by_date,
    toggle_task_completion,
    update_task,
)

logger = logging.getLogger(__name__)

api_tasks = Blueprint("api", __name__, url_prefix="/api/tasks")

@api_tasks.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id_from_jwt = get_jwt_identity()
    result = get_all_tasks(user_id=user_id_from_jwt)
    return jsonify(result), result.get("status_code", 200)

@api_tasks.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task_by_id(task_id):
    user_id_from_jwt = get_jwt_identity()  # Cambiado de current_user.id
    result = get_task_by_id(task_id, user_id=user_id_from_jwt)
    return jsonify(result), result.get("status_code", 200)

@api_tasks.route("/", methods=["POST"])
@jwt_required()
def create_new_task():
    try:
        user_id_from_jwt = get_jwt_identity()
        data = request.get_json()
        
        result = create_task(
            title=data.get('title'),
            description=data.get('description'),
            due_date=data.get('due_date'),
            priority_id=data.get('priority_id'),
            category_id=data.get('category_id'),
            user_id=user_id_from_jwt
        )
        
        return jsonify(result), result.get("status_code", 201)
    
    except Exception as e:
        logger.error(f"Error en endpoint de creación: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error procesando la solicitud",
            "errors": {"request": "Error en los datos de entrada"},
            "status_code": 400
        }), 400

@api_tasks.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_existing_task(task_id):
    user_id_from_jwt = get_jwt_identity()
    data = request.get_json()
    
    result = update_task(
        task_id=task_id,
        title=data.get('title'),
        description=data.get('description'),
        due_date=data.get('due_date'),
        priority_id=data.get('priority_id'),
        category_id=data.get('category_id'),
        user_id=user_id_from_jwt
    )
    
    return jsonify(result), result.get("status_code", 200)

@api_tasks.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task_endpoint(task_id):
    """Endpoint para eliminar una tarea"""
    user_id_from_jwt = get_jwt_identity()
    result = delete_task(
        task_id=task_id,
        user_id=user_id_from_jwt
    )
    return jsonify(result), result.get("status_code", 200)

@api_tasks.route("/<int:task_id>/toggle", methods=["PATCH"])
@jwt_required()
def toggle_task_status(task_id):
    user_id_from_jwt = get_jwt_identity()  # Cambiado de current_user.id
    result = toggle_task_completion(
        task_id=task_id,
        user_id=user_id_from_jwt
    )
    return jsonify(result), result.get("status_code", 200)

@api_tasks.route("/tasks/completed", methods=["GET"])
@jwt_required()
def get_completed_tasks_api():  # Removido parámetro user_id
    user_id_from_jwt = get_jwt_identity()  # Cambiado de current_user.id
    result = get_completed_tasks(user_id=user_id_from_jwt)
    return jsonify(result), result.get("status_code", 200)


@api_tasks.route("/tasks/pending", methods=["GET"])
@jwt_required()
def get_pending_tasks_api():  # Removido parámetro user_id
    user_id_from_jwt = get_jwt_identity()  # Cambiado de current_user.id
    result = get_pending_tasks(user_id=user_id_from_jwt)  # Cambiado de get_completed_tasks
    return jsonify(result), result.get("status_code", 200)

@api_tasks.route("/by-date/<string:fecha>", methods=["GET"])
@jwt_required()
def get_tasks_for_date(fecha):
    user_id_from_jwt = get_jwt_identity()  # Cambiado de current_user.id
    result = get_tasks_by_date(user_id_from_jwt, fecha)
    return jsonify(result), result.get("status_code", 200)
