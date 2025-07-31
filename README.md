# 📋 Task Manager

**Task Manager** es una aplicación web moderna para la gestión de tareas y proyectos, desarrollada con **Flask** (backend), **Tailwind CSS** (frontend) y **SweetAlert2** (modales y alertas). Permite crear, editar, eliminar, filtrar y marcar tareas como completadas, con autenticación de usuarios y una experiencia visual atractiva y responsiva.

---

## 🚀 Características principales

- **Gestión de tareas**: Crear, editar, eliminar, filtrar y marcar tareas como completadas.
- **Autenticación de usuarios**: Registro, login y logout seguro con Flask-Login.
- **Categorías y prioridades**: Clasificación de tareas por categoría y prioridad.
- **Interfaz moderna**: UI responsiva con Tailwind CSS.
- **Modales y alertas**: Experiencia de usuario mejorada con SweetAlert2 para validaciones, confirmaciones, carga y éxito/error.
- **Mensajes animados**: Confirmaciones y errores con animaciones y cierre automático.
- **Carga dinámica**: CRUD de tareas vía API y JavaScript modular (ES6).
- **Filtros y búsqueda**: Filtrado de tareas por estado (todas, pendientes, completadas).
- **Modal para crear/editar**: Formulario en modal para una experiencia fluida.
- **Logs y seguridad**: Manejo de errores, validaciones y logs en backend.

---

## 🖥️ Capturas de pantalla

> (Agrega aquí capturas de la interfaz principal, modales y alertas si lo deseas)

---

## 🗂️ Estructura del proyecto

```
Task-Manager/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   │   └── js/
│   │       └── task/
│   ├── templates/
│   └── utils/
│
├── config.py
├── requirements.txt
├── run.py
├── task_db.sql
└── test_loading_modal.html
```

---

## ⚙️ Instalación y ejecución

1. **Clona el repositorio**  
   ```bash
   git clone <URL-del-repo>
   cd Task-Manager
   ```

2. **Crea y activa un entorno virtual**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos**  
   - Ejecuta el script SQL `task_db.sql` para crear las tablas.
   - (Opcional) Usa los scripts de carga para datos de prueba si los tienes.

5. **Ejecuta la aplicación**  
   ```bash
   python run.py
   ```
   Accede a [http://localhost:5000](http://localhost:5000) en tu navegador.

---

## 🧩 Tecnologías utilizadas

- **Backend**: Flask, Flask-Login, SQLAlchemy
- **Frontend**: Tailwind CSS, HTML5, JavaScript (ES6 Modules)
- **Modales/Alertas**: SweetAlert2
- **Base de datos**: SQLite (por defecto, fácilmente adaptable)
- **Otros**: Logging, validaciones, manejo de errores

---

## 📦 Estructura de los módulos JS

- `task-model.js`: Lógica de datos y comunicación con la API.
- `task-view.js`: Renderizado, modales y mensajes con SweetAlert2.
- `task-controller.js`: Coordinación de eventos y lógica de negocio.
- `task-manager.js`: Punto de entrada e inicialización.

---

## 📝 Convenciones y buenas prácticas

- Código modular y documentado.
- Validaciones tanto en frontend como en backend.
- Manejo de errores y logs en formato JSON.
- UI accesible y responsiva.
- Uso de ES6+ y Tailwind para un desarrollo moderno.

---

## 🛡️ Seguridad

- Contraseñas hasheadas y autenticación segura.
- Validación de datos en todos los endpoints.
- Protección contra CSRF y XSS.

---


---

¿Quieres agregar algo más específico (por ejemplo, instrucciones de despliegue, contribución, o detalles de endpoints API)? ¡Dímelo y lo incluyo! 