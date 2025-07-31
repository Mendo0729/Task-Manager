from datetime import datetime
import logging

from click.formatting import measure_table
from sqlalchemy.exc import SQLAlchemyError

from app.models.task import Tasks
from app.utils.create_responses import create_response
from app.utils.db import db

logger = logging.getLogger(__name__)

# -------------------- Mostrar tareas --------------------

def get_all_tasks(user_id):
    try:
        if not user_id:
            return create_response(
                success=False,
                message="user_id es requerido",
                errors={
                    "code": "missing_fields",
                    "detail": "Todos los campos son requeridos"
                },
                status_code=400
            )
        tareas = Tasks.query.filter_by(user_id=user_id).all()
        serialized_tasks = [tarea.to_dict() for tarea in tareas]
        if not tareas:
            logger.info(f"Obtenidas {len(tareas)} tareas para usuario {user_id}")
            return create_response(
                success=True,
                message=f"No hay tareas",
                data=[],
                status_code=200
            )
        logger.info(f"Obtenidas {len(tareas)} tareas ")
        return create_response(
            success=True,
            message=f"Tareas obtenidas exitosamente",
            data=serialized_tasks,
            status_code=200
        )
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener las tareas: {str(e)}")
        return create_response(
            success=True,
            message= "Error de base de datos al obtener la tarea",
            errors={
                "code": "database_error",
                "detail": str(e)
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener las tarea: {str(e)}")
        return create_response(
            success=False,
            message="Error interno al obtener la tarea",
            errors={"server": "Error interno del servidor"},
            status_code=500
        )

def get_task_by_id(task_id, user_id=None):
    try:
        if not task_id:
            return create_response(
                success=False,
                message="ID de tarea no proporcionado",
                errors={"task_id": "El ID de la tarea es requerido"},
                status_code=400
            )

        query = Tasks.query.filter_by(task_id=task_id)
        if user_id:
            query = query.filter_by(user_id=user_id)

        task = query.first()
        
        if not task:
            error_msg = "Tarea no encontrada"
            if user_id:
                error_msg = "Tarea no encontrada o no pertenece al usuario"
            return create_response(
                success=False,
                message=error_msg,
                errors={"not_found": error_msg},
                status_code=404
            )

        task_data = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description or "",
            "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            "is_completed": task.is_completed,
            "priority_id": task.priority_id,
            "category_id": task.category_id,
            "created_at": task.created_at.strftime('%Y-%m-%d %H:%M:%S') if task.created_at else None,
            "user_id": task.user_id
        }

        return create_response(
            success=True,
            data=task_data,
            message="Tarea obtenida exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error al obtener la tarea {task_id}: {str(e)}")
        return create_response(
            success=False,
            message="Error de base de datos al obtener la tarea",
            errors={"database": str(e)},
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener tarea {task_id}: {str(e)}")
        return create_response(
            success=False,
            message="Error interno al obtener la tarea",
            errors={"server": "Error interno del servidor"},
            status_code=500
        )

def get_tasks_by_date(user_id, fecha):

    try:
        # Validación de parámetros
        if not user_id:
            return create_response(
                success=False,
                message="ID de usuario no proporcionado",
                errors={"user_id": "El ID de usuario es requerido"},
                status_code=400
            )
        
        if not fecha:
            return create_response(
                success=False,
                message="Fecha no proporcionada",
                errors={"fecha": "La fecha es requerida"},
                status_code=400
            )

        # Convertir fecha si es string (opcional, dependiendo de tu necesidad)
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            except ValueError:
                return create_response(
                    success=False,
                    message="Formato de fecha inválido",
                    errors={"fecha": "El formato debe ser YYYY-MM-DD"},
                    status_code=400
                )

        # Consulta a la base de datos
        tareas = Tasks.query.filter_by(user_id=user_id, due_date=fecha).all()
        
        logger.info(f"Obtenidas {len(tareas)} tareas para fecha {fecha}")
        
        # Serializar las tareas
        tareas_serializadas = [{
            "id": t.task_id,
            "title": t.title,
            "description": t.description or "",
            "due_date": t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            "is_completed": t.is_completed,
            "priority_id": t.priority_id,
            "category_id": t.category_id,
            "created_at": t.created_at.strftime('%Y-%m-%d %H:%M:%S') if t.created_at else None,
            "user_id": t.user_id
        } for t in tareas]

        return create_response(
            success=True,
            data=tareas_serializadas,
            message=f"Se encontraron {len(tareas_serializadas)} tareas para la fecha {fecha}",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener tareas por fecha: {str(e)}")
        return create_response(
            success=False,
            message="Error al obtener las tareas",
            errors={"database": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener tareas por fecha: {str(e)}")
        return create_response(
            success=False,
            message="Error interno del servidor",
            errors={"server": "Error interno"},
            status_code=500
        )

def get_completed_tasks(user_id):
    if not user_id:
            return create_response(
                success=False,
                message="ID de usuario no proporcionado",
                errors={"user_id": "El ID de usuario es requerido"},
                status_code=400
            )
    
    try:
        tareas = Tasks.query.filter_by(user_id=user_id, is_completed=True).all()
        if not tareas:
            return create_response(
                success=True,
                message="No hay tareas Pendientes",
                data=[],
                status_code=200
            )     
        logger.info(f"Obtenidas {len(tareas)} tareas completadas para usuario {user_id}")

        tareas_serializadas = [{
            "id": t.task_id,
            "title": t.title,
            "description": t.description or "",
            "due_date": t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            "is_completed": t.is_completed,
            "priority_id": t.priority_id,
            "category_id": t.category_id,
            "created_at": t.created_at.strftime('%Y-%m-%d %H:%M:%S') if t.created_at else None,
            "user_id": t.user_id
        } for t in tareas]

        return create_response(
            success=True,
            data=tareas_serializadas,
            message=f"Se encontraron {len(tareas_serializadas)} tareas completadas",
            status_code=200
        )
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener tareas completadas: {str(e)}")
        return create_response(
            success=False,
            message="Error al obtener las tareas",
            errors={"database": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener tareas cmpletadas: {str(e)}")
        return create_response(
            success=False,
            message="Error interno del servidor",
            errors={"server": "Error interno"},
            status_code=500
        )

#--------------------------------------- Obtener tareas pendientes ------------------------------------------

def get_pending_tasks(user_id):
    if not user_id:
            return create_response(
                success=False,
                message="ID de usuario no proporcionado",
                errors={"user_id": "El ID de usuario es requerido"},
                status_code=400
            )
    
    try:
        tareas = Tasks.query.filter_by(user_id=user_id, is_completed=False).all()
        if not tareas:
            return create_response(
                success=True,
                message="No hay tareas completadas",
                data={"tasks": {}},
                status_code=200
            )
        logger.info(f"Obtenidas {len(tareas)} tareas pendientes para usuario {user_id}")

        tareas_serializadas = [{
            "id": t.task_id,
            "title": t.title,
            "description": t.description or "",
            "due_date": t.due_date.strftime('%Y-%m-%d') if t.due_date else None,
            "is_completed": t.is_completed,
            "priority_id": t.priority_id,
            "category_id": t.category_id,
            "created_at": t.created_at.strftime('%Y-%m-%d %H:%M:%S') if t.created_at else None,
            "user_id": t.user_id
        } for t in tareas]

        return create_response(
            success=True,
            data=tareas_serializadas,
            message=f"Se encontraron {len(tareas_serializadas)} tareas pendientes",
            status_code=200
        )
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener tareas pendientes: {str(e)}")
        return create_response(
            success=False,
            message="Error al obtener las tareas",
            errors={"database": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener tareas pendientes: {str(e)}")
        return create_response(
            success=False,
            message="Error interno del servidor",
            errors={"server": "Error interno"},
            status_code=500
        )

# -------------------- Crear tareas --------------------

def create_task(title, description, due_date, priority_id, category_id, user_id):
    # Validaciones de entrada
    if not title or not title.strip():
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"title": "El título es requerido"},
            status_code=400
        )
    
    if not user_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"user_id": "El ID de usuario es requerido"},
            status_code=400
        )
    
    if not priority_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"priority_id": "El ID de prioridad es requerido"},
            status_code=400
        )
    
    if not category_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"category_id": "El ID de categoría es requerido"},
            status_code=400
        )

    try:
        # Convertir fecha si es string (opcional)
        if isinstance(due_date, str):
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            except ValueError:
                return create_response(
                    success=False,
                    message="Formato de fecha inválido",
                    errors={"due_date": "El formato debe ser YYYY-MM-DD"},
                    status_code=400
                )

        new_task = Tasks(
            title=title.strip(),
            description=description.strip() if description else "",
            due_date=due_date,
            priority_id=priority_id,
            category_id=category_id,
            user_id=user_id
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        logger.info(f"Tarea creada exitosamente: {title} para usuario {user_id}")
        
        # Serializar la tarea creada
        task_data = {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "due_date": new_task.due_date.strftime('%Y-%m-%d') if new_task.due_date else None,
            "priority_id": new_task.priority_id,
            "category_id": new_task.category_id,
            "user_id": new_task.user_id,
            "created_at": new_task.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_task.created_at else None
        }
        
        return create_response(
            success=True,
            data=task_data,
            message="Tarea creada exitosamente",
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al crear tarea: {str(e)}")
        return create_response(
            success=False,
            message="Error al crear la tarea",
            errors={"database": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al crear tarea: {str(e)}")
        return create_response(
            success=False,
            message="Error interno del servidor",
            errors={"server": "Error interno"},
            status_code=500
        )

# -------------------- Actualizar y eliminar tareas --------------------

def update_task(task_id, title, description, due_date, priority_id, category_id, user_id):

    if not user_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"user_id": "El ID de usuario es requerido"},
            status_code=400
        )
    if not title or not title.strip():
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"title": "El título es requerido"},
            status_code=400
        )

    if not priority_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"priority_id": "El ID de prioridad es requerido"},
            status_code=400
        )
    
    if not category_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"category_id": "El ID de categoría es requerido"},
            status_code=400
        )
    
    try:
        # Verificar que la tarea existe y pertenece al usuario
        tarea = Tasks.query.filter_by(task_id=task_id, user_id=user_id).first()
        if not tarea:
            return create_response(
                success=False,
                message="Tarea no encontrada",
                errors={
                    "code": "not_found_task",
                    "detail": "Tarea no encontrada"
                },
                status_code=400
            )
        
        tarea.title = title.strip()
        tarea.description = description.strip() if description else ""
        tarea.due_date = due_date
        tarea.priority_id = priority_id
        tarea.category_id = category_id

        db.session.commit()
        logger.info(f"Tarea actualizada exitosamente: {title}")

        updated_task = {
            "id": tarea.task_id,
            "title": tarea.title,
            "description": tarea.description,
            "due_date": tarea.due_date.strftime('%Y-%m-%d') if tarea.due_date else None,
            "priority_id": tarea.priority_id,
            "category_id": tarea.category_id,
            "user_id": tarea.user_id,
            "is_completed": tarea.is_completed,
            "created_at": tarea.created_at.strftime('%Y-%m-%d %H:%M:%S') if tarea.created_at else None,
            "updated_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        return create_response(
            success=True,
            data=updated_task,
            message="Tarea actualida exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al actualizar la tarea: {str(e)}")
        return create_response(
            success=False,
            message="Error al actualizar la tarea",
            errors={"database": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al actualizar la tarea: {str(e)}")
        return create_response(
            success=False,
            message="Error interno del servidor",
            errors={"server": "Error interno"},
            status_code=500
        )

def delete_task(task_id, user_id):
    # Validaciones de entrada
    if not task_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"task_id": "El ID de tarea es requerido"},
            status_code=400
        )
    
    if not user_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"user_id": "El ID de usuario es requerido"},
            status_code=400
        )

    try:
        # Verificar que la tarea existe y pertenece al usuario
        tarea = Tasks.query.filter_by(task_id=task_id, user_id=user_id).first()
        
        if not tarea:
            return create_response(
                success=False,
                message="Operación no permitida",
                errors={
                    "not_found": f"No se encontró la tarea con ID {task_id} para el usuario {user_id}"
                },
                status_code=404
            )
        
        # Guardar datos para el log antes de eliminar
        task_title = tarea.title
        task_user = tarea.user_id
        
        db.session.delete(tarea)
        db.session.commit()
        
        logger.info(f"Tarea '{task_title}' (ID: {task_id}) eliminada por usuario {task_user}")
        
        return create_response(
            success=True,
            data={
                "id": task_id,
                "deleted_at": datetime.utcnow().isoformat()
            },
            message="Tarea eliminada exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al eliminar tarea {task_id}: {str(e)}")
        return create_response(
            success=False,
            message="Error al eliminar la tarea",
            errors={"database": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al eliminar tarea {task_id}: {str(e)}")
        return create_response(
            success=False,
            message="Error interno del servidor",
            errors={"server": "Error interno"},
            status_code=500
        )

def toggle_task_completion(task_id, user_id):
    # Validaciones de entrada
    if not task_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"task_id": "El ID de tarea es requerido"},
            status_code=400
        )
    
    if not user_id:
        return create_response(
            success=False,
            message="Validación fallida",
            errors={"user_id": "El ID de usuario es requerido"},
            status_code=400
        )

    try:
        # Buscar la tarea verificando pertenencia al usuario
        tarea = Tasks.query.filter_by(task_id=task_id, user_id=user_id).first()
        
        if not tarea:
            return create_response(
                success=False,
                message="Operación no permitida",
                errors={
                    "not_found": f"No se encontró la tarea con ID {task_id} para el usuario {user_id}"
                },
                status_code=404
            )
        
        # Cambiar el estado
        tarea.is_completed = not tarea.is_completed
        nuevo_estado = "completada" if tarea.is_completed else "pendiente"
        db.session.commit()
        
        logger.info(f"Tarea {task_id} marcada como {nuevo_estado} por usuario {user_id}")
        
        # Preparar respuesta con datos actualizados
        task_data = {
            "id": tarea.task_id,
            "title": tarea.title,
            "is_completed": tarea.is_completed,
            "status": nuevo_estado,
            "updated_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return create_response(
            success=True,
            data=task_data,
            message=f"Tarea marcada como {nuevo_estado} exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al cambiar estado de tarea {task_id}: {str(e)}")
        return create_response(
            success=False,
            message="Error al actualizar el estado",
            errors={"database": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al cambiar estado de tarea {task_id}: {str(e)}")
        return create_response(
            success=False,
            message="Error interno del servidor",
            errors={"server": "Error interno"},
            status_code=500
        )