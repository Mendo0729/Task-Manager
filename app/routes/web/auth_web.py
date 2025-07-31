# app/routes/auth_views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests

auth_views = Blueprint('auth_views', __name__)

API_BASE = "http://localhost:5000/api/auth"  # Cambia esto si usas Docker o Nginx como proxy

@auth_views.route('/')
def index():
    return redirect(url_for('auth_views.login_view'))


@auth_views.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        response = requests.post(f"{API_BASE}/login", json={
            "username": username,
            "password": password
        })

        result = response.json()

        if result.get("success"):
            session['access_token'] = result.get("access_token")
            session['user_id'] = result.get("data", {}).get("id")
            session['username'] = result.get("data", {}).get("username")
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('task_views.index'))  # ajusta según tu vista principal
        else:
            flash(result.get("message", "Error al iniciar sesión"), "danger")

    return render_template('auth/login.html')


@auth_views.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for('auth_views.login_view'))


@auth_views.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        response = requests.post(f"{API_BASE}/register", json={
            "username": username,
            "email": email,
            "password": password
        })

        result = response.json()

        if result.get("success"):
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('auth_views.login_view'))
        else:
            flash(result.get("message", "Error al registrar"), "danger")

    return render_template('auth/register.html')
