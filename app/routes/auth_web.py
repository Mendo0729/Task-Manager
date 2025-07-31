"""from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    flash,
    render_template,
    current_app
)
from app.services.auth_services import (
    register_user,
    validate_user
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from app import login_manager
from app.utils.db import db
from app.models.user import User
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Validar que los campos no estén vacíos
        if not username or not password:
            flash("Usuario y contraseña requeridos", "error")
            return redirect(url_for("auth.login"))
        
        try:
            # Validar credenciales
            user = validate_user(username, password)
            
            if user:
                login_user(user)
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for("tasks.index"))
            
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("auth.login"))
        
        # Si llegamos aquí, las credenciales son incorrectas
        flash("Credenciales incorrectas", "error")
        return redirect(url_for("auth.login"))
    
    # Método GET - mostrar formulario de login
    return render_template("auth/login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validaciones básicas
        if not email or not username or not password:
            flash("Correo, usuario y contraseña requeridos", "error")
            return redirect(url_for("auth.register"))
        
        if password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for("auth.register"))
        
        try:
            user = register_user(username, password, email)
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for("auth.login"))
        
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("auth.register"))
    
    # Método GET - mostrar formulario de registro
    return render_template("auth/register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("auth.login"))

def generate_reset_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='password-reset-salt')

def confirm_reset_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return None
    return email

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Por favor ingresa tu correo electrónico', 'error')
            return redirect(url_for('auth.forgot_password'))
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No existe una cuenta con ese correo', 'error')
            return redirect(url_for('auth.forgot_password'))
        token = generate_reset_token(email)
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        print(f"[RECUPERACIÓN] Enlace para restablecer contraseña: {reset_url}")
        flash('Se ha enviado un enlace de recuperación a tu correo (simulado)', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = confirm_reset_token(token)
    if not email:
        flash('El enlace es inválido o ha expirado', 'error')
        return redirect(url_for('auth.forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not password or not confirm_password:
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('auth.reset_password', token=token))
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.reset_password', token=token))
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('auth.forgot_password'))
        user.set_password(password)
        db.session.commit()
        flash('Contraseña restablecida exitosamente', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', token=token)
"""