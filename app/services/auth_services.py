import logging
import time

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User
from app.utils.create_responses import create_response
from app.utils.db import db

# Configurar logger específico para este módulo
logger = logging.getLogger(__name__)

def register_user(username, password, email):
    try:

        if not username or not password or not email:
            return create_response(
                success=False,
                message="El nombre de usuario, el correo electrónico y la contraseña son requeridos",
                errors={
                    "code": "missing_fields",
                    "detail": "Todos los campos son requeridos",
                    "fields": ["username", "email", "password"]
                    },
                status_code=400
            )

        if User.query.filter_by(username=username).first():
            return create_response(
                success=False,
                message="El nombre de usuario ya existe",
                errors={
                    "code": "username_exists",
                    "detail": "El nombre de usuario ya está registrado"
                },
                status_code=400
            )

        if User.query.filter_by(email=email).first():
            return create_response(
                success=False,
                message="El email ya existe",
                errors={
                    "code": "email_exists",
                    "detail": "El email ya está registrado"
                },
                status_code=400
            )

        new_user = User(username=username, email=email) # type: ignore
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"Usuario registrado exitosamente: {username} ({email})")
        return create_response(
            success=True,
            message="Usuario registrado exitosamente",
            data={
                "username": username,
                "email": email
            },
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error al registrar el usuario {username}: {str(e)}")
        return create_response(
            success=False,
            message="Error al registrar el usuario",
            errors={"code": "database_error", "detail": str(e)},
            status_code=500
        )

def validate_user(username, password):

    if not username or not password:
        return create_response(
            success=False,
            message="El nombre de usuario y la contraseña son requeridos",
            errors={"code": "missing_fields", "detail": "El nombre de usuario y la contrasena son requeridos"},
            status_code=400
        )

    try:
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            time.sleep(0.5)  # Protección contra ataques de fuerza bruta
            logger.warning(f"Intento de login fallido para usuario: {username}")
            return create_response(
                success=False,
                message="Nombre de usuario o contraseña incorrectos",
                errors={"code": "invalid_credentials", "detail": "Nombre de usuario o contraseña incorrectos"},
                status_code=401
            )
        logger.info(f"Usuario autenticado exitosamente: {username}")
        return create_response(
            success=True,
            data={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                },
            message="Usuario autenticado exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error al validar el usuario {username}: {str(e)}")
        return create_response(
            success=False,
            message="Error al validar el usuario",
            errors={"code": "database_error", "detail": str(e)},
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener las tarea: {str(e)}")
        return create_response(
            success=False,
            message="Error interno al validar el usuario",
            errors={"server": "Error interno del servidor"},
            status_code=500
        ) 